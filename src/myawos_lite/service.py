from __future__ import annotations

import json
import logging
import signal
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import state_path
from .hardware import AirspyReceiver, ClickDetector, UsbRelay
from .voice import build_announcement, write_observation
from .weather import fetch


LOGGER = logging.getLogger("myawos-lite")
UNAVAILABLE_AUDIO_NAME = "WeatherStation_no_weather_available_at_this_time.wav"


def weather_audio_for_transmission(
    config: dict[str, Any], now: datetime | None = None
) -> tuple[Path, bool]:
    """Return the safe announcement path and whether weather is unavailable."""
    current_audio = state_path(config, "current.wav")
    observation_file = state_path(config, "current-weather.json")
    unavailable_audio = Path(config["paths"]["media_directory"]) / UNAVAILABLE_AUDIO_NAME
    max_age_hours = float(config["weather"].get("max_age_hours", 12))
    if max_age_hours <= 0:
        raise ValueError("weather.max_age_hours must be greater than zero")

    current_time = now or datetime.now(timezone.utc)
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    try:
        data = json.loads(observation_file.read_text(encoding="utf-8"))
        observed_at = datetime.fromisoformat(str(data["observed_at"]))
        if observed_at.tzinfo is None:
            observed_at = observed_at.replace(tzinfo=timezone.utc)
        age_hours = (current_time - observed_at.astimezone(timezone.utc)).total_seconds() / 3600
        stale = age_hours >= max_age_hours
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        LOGGER.warning("Weather observation metadata is missing or invalid: %s", error)
        stale = True

    if current_audio.is_file() and not stale:
        return current_audio, False
    return unavailable_audio, True


class WeatherWorker(threading.Thread):
    def __init__(self, config: dict[str, Any]):
        super().__init__(daemon=True, name="weather-refresh")
        self.config = config
        self.stop_event = threading.Event()

    def refresh(self) -> None:
        observation = fetch(self.config)
        output = state_path(self.config, "current.wav")
        media = Path(self.config["paths"]["media_directory"])
        build_announcement(observation, media, output)
        write_observation(observation, state_path(self.config, "current-weather.json"))
        LOGGER.info("Weather refreshed for %s", observation.observed_at.isoformat())

    def run(self) -> None:
        interval = max(30, int(self.config["weather"].get("refresh_seconds", 60)))
        while not self.stop_event.is_set():
            try:
                self.refresh()
            except Exception:
                LOGGER.exception(
                    "Weather refresh failed; last observation remains subject to the age limit"
                )
            self.stop_event.wait(interval)


class RadioTransmitter:
    def __init__(self, config: dict[str, Any], receiver: AirspyReceiver):
        self.config = config
        self.receiver = receiver
        self.relay = UsbRelay(config["relay"])

    def transmit(self) -> None:
        if not bool(self.config["transmitter"].get("enabled", False)):
            LOGGER.info("Weather request received; transmission is disabled")
            return
        audio, unavailable = weather_audio_for_transmission(self.config)
        if not audio.is_file():
            LOGGER.error("Weather request ignored: required announcement %s is missing", audio)
            return
        if unavailable:
            LOGGER.warning("Weather request accepted with unavailable-weather announcement")
        else:
            LOGGER.info("Weather request accepted")
        self.receiver.stop()
        try:
            self.relay.set(False)
            self.relay.set(True)
            time.sleep(float(self.config["transmitter"].get("ptt_lead_seconds", 0.5)))
            command = [
                "aplay", "-q", "-D", str(self.config["transmitter"]["audio_device"]), str(audio)
            ]
            subprocess.run(
                command,
                check=True,
                timeout=float(self.config["transmitter"].get("max_seconds", 60)),
            )
            time.sleep(float(self.config["transmitter"].get("ptt_tail_seconds", 0.3)))
        except Exception:
            LOGGER.exception("Radio transmission failed")
        finally:
            try:
                self.relay.set(False)
            finally:
                self.relay.close()
                time.sleep(float(self.config["receiver"].get("restart_delay_seconds", 0.5)))
                self.receiver.start()
        request_log = state_path(self.config, "requests.jsonl")
        request_log.parent.mkdir(parents=True, exist_ok=True)
        with request_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"time": datetime.now(timezone.utc).isoformat()}) + "\n")


def run(config: dict[str, Any]) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    state_dir = Path(config["paths"]["state_directory"])
    state_dir.mkdir(parents=True, exist_ok=True)

    receiver = AirspyReceiver(config)
    relay = UsbRelay(config["relay"])
    try:
        relay.set(False)
    finally:
        relay.close()

    worker = WeatherWorker(config)
    worker.start()
    receiver.start()
    transmitter = RadioTransmitter(config, receiver)
    detector = ClickDetector(config, LOGGER)

    def stop_service(_signum: int, _frame: object) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop_service)
    signal.signal(signal.SIGINT, stop_service)
    LOGGER.info("Listening on %.3f MHz for %d clicks", float(config["radio"]["frequency_mhz"]), int(config["radio"]["required_clicks"]))
    try:
        detector.run(receiver, transmitter.transmit)
    except KeyboardInterrupt:
        LOGGER.info("Stopping MyAWOS Lite")
    finally:
        worker.stop_event.set()
        receiver.stop()
        try:
            relay.set(False)
        finally:
            relay.close()
