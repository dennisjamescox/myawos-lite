from __future__ import annotations

import glob
import logging
import shutil
import subprocess
import time
from collections import deque
from pathlib import Path
from typing import Any, Callable

import numpy as np
import serial


class AirspyReceiver:
    unit = "RMS"

    def __init__(self, config: dict[str, Any]):
        receiver = config["receiver"]
        radio = config["radio"]
        self.command = [
            "airspy_rx",
            "-f", str(radio["frequency_mhz"]),
            "-a", str(int(receiver.get("sample_rate", 2_500_000))),
            "-r", "-",
        ]
        serial_number = str(receiver.get("serial", "auto")).strip()
        if serial_number and serial_number != "auto":
            self.command.extend(["-s", serial_number])
        self.chunk_bytes = int(receiver.get("chunk_bytes", 8192))
        self.process: subprocess.Popen[bytes] | None = None

    def start(self) -> None:
        if shutil.which(self.command[0]) is None:
            raise RuntimeError("airspy_rx is not installed")
        self.process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0,
        )

    def stop(self) -> None:
        if self.process is None:
            return
        process = self.process
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
        if process.stdout is not None:
            process.stdout.close()
        self.process = None

    def read_level(self) -> float:
        if self.process is None or self.process.stdout is None:
            raise RuntimeError("Airspy receiver is not running")
        data = self.process.stdout.read(self.chunk_bytes)
        if not data:
            raise RuntimeError(f"Airspy stream ended (status {self.process.poll()})")
        samples = np.frombuffer(data, dtype=np.int16)
        if not samples.size:
            return 0.0
        return float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))


def find_relay_port(configured: str) -> str | None:
    if configured and configured != "auto":
        return configured if Path(configured).exists() else None
    candidates = sorted(glob.glob("/dev/serial/by-id/*")) + sorted(glob.glob("/dev/ttyUSB*"))
    return candidates[0] if candidates else None


class UsbRelay:
    def __init__(self, settings: dict[str, Any]):
        self.settings = settings
        self.connection: serial.Serial | None = None

    def open(self) -> None:
        port = find_relay_port(str(self.settings.get("port", "auto")))
        if not port:
            raise RuntimeError("USB relay was not found")
        self.connection = serial.Serial(port, int(self.settings.get("baud", 9600)), timeout=1)
        time.sleep(0.15)

    def set(self, enabled: bool) -> None:
        if self.connection is None or not self.connection.is_open:
            self.open()
        assert self.connection is not None
        key = "on_command_hex" if enabled else "off_command_hex"
        self.connection.write(bytes.fromhex(str(self.settings[key])))
        self.connection.flush()

    def close(self) -> None:
        if self.connection is not None and self.connection.is_open:
            self.connection.close()


class ClickDetector:
    def __init__(self, config: dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger

    def run(self, receiver: AirspyReceiver, trigger: Callable[[], None]) -> None:
        radio = self.config["radio"]
        settings = self.config["receiver"]
        required = int(radio.get("required_clicks", 5))
        window = float(radio.get("click_window_seconds", 4))
        cooldown = float(radio.get("cooldown_seconds", 30))
        min_gap = float(settings.get("min_click_gap_seconds", 0.2))
        min_quiet = float(settings.get("min_quiet_time_seconds", 0.12))
        calibration_samples = int(settings.get("calibration_samples", 700))
        on_ratio = float(settings.get("threshold_on_ratio", 4.0))
        off_ratio = float(settings.get("threshold_off_ratio", 2.5))

        levels: list[float] = []
        noise_floor: float | None = None
        click_times: deque[float] = deque()
        carrier_active = False
        quiet_since = time.monotonic()
        last_click = 0.0
        last_trigger = 0.0

        while True:
            level = receiver.read_level()
            now = time.monotonic()
            if noise_floor is None:
                levels.append(level)
                if len(levels) < calibration_samples:
                    continue
                noise_floor = max(float(np.median(levels)), 1.0)
                self.logger.info("Airspy calibrated: noise %.1f RMS", noise_floor)

            on_threshold = noise_floor * on_ratio
            off_threshold = noise_floor * off_ratio
            if carrier_active:
                if level < off_threshold:
                    carrier_active = False
                    quiet_since = now
                continue

            if level < off_threshold:
                noise_floor = 0.997 * noise_floor + 0.003 * level
            if level <= on_threshold or now - quiet_since < min_quiet or now - last_click < min_gap:
                continue

            carrier_active = True
            last_click = now
            click_times.append(now)
            while click_times and now - click_times[0] > window:
                click_times.popleft()
            self.logger.info("Click %d/%d level=%.1f RMS", len(click_times), required, level)

            if len(click_times) < required:
                continue
            click_times.clear()
            if now - last_trigger < cooldown:
                self.logger.info("Request ignored during cooldown")
                continue
            last_trigger = now
            trigger()
            levels.clear()
            noise_floor = None
            carrier_active = False
            quiet_since = time.monotonic()
            last_click = 0.0
