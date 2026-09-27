from __future__ import annotations

import argparse
import glob
import grp
import json
import os
import shutil
import subprocess
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

from .config import DEFAULT_CONFIG, load_config, state_path
from .hardware import UsbRelay, find_relay_port
from .models import WeatherObservation
from .service import WeatherWorker, run
from .voice import build_announcement
from .weather import fetch


def _config_path(value: str | None) -> Path:
    return Path(value) if value else DEFAULT_CONFIG


def command_doctor(config: dict) -> int:
    checks: list[tuple[str, bool, str]] = []
    for executable in ("airspy_rx", "airspy_info", "aplay"):
        location = shutil.which(executable)
        checks.append((executable, bool(location), location or "not installed"))
    relay = find_relay_port(str(config["relay"].get("port", "auto")))
    checks.append(("USB relay", bool(relay), relay or "not found"))
    media = Path(config["paths"]["media_directory"])
    checks.append(("Voice media", media.is_dir(), str(media)))
    try:
        observation = fetch(config)
        checks.append(("Weather source", True, observation.observed_at.isoformat()))
    except Exception as exc:
        checks.append(("Weather source", False, str(exc)))
    failed = False
    for name, passed, detail in checks:
        failed |= not passed
        print(f"{'PASS' if passed else 'FAIL':4}  {name}: {detail}")
    print(f"INFO  Automatic transmission: {'ENABLED' if config['transmitter'].get('enabled') else 'disabled'}")
    return 1 if failed else 0


def command_devices() -> int:
    print("Serial relay candidates:")
    ports = sorted(glob.glob("/dev/serial/by-id/*")) + sorted(glob.glob("/dev/ttyUSB*"))
    for port in ports or ["(none)"]:
        print(f"  {port}")
    print("\nALSA playback devices:")
    subprocess.run(["aplay", "-l"], check=False)
    print("\nAirspy devices:")
    subprocess.run(["airspy_info"], check=False)
    return 0


def detect_audio_device() -> str:
    result = subprocess.run(["aplay", "-l"], text=True, capture_output=True, check=False)
    matches = re.findall(r"card \d+: ([^ ]+) \[[^]]+\], device (\d+):", result.stdout)
    if not matches:
        return "default"
    preferred = next(((card, device) for card, device in matches if card.upper() not in {"PCH", "HDMI"}), matches[0])
    return f"plughw:CARD={preferred[0]},DEV={preferred[1]}"


def command_generate(config: dict) -> int:
    observation = fetch(config)
    output = state_path(config, "current.wav")
    tokens = build_announcement(observation, Path(config["paths"]["media_directory"]), output)
    print(f"Created {output}")
    print("Voice sequence:", " ".join(tokens))
    return 0


def command_play(config: dict) -> int:
    audio = state_path(config, "current.wav")
    if not audio.is_file():
        raise FileNotFoundError(f"Generate weather audio first: {audio}")
    return subprocess.run(
        ["aplay", "-D", str(config["transmitter"]["audio_device"]), str(audio)], check=False
    ).returncode


def command_relay_off(config: dict) -> int:
    relay = UsbRelay(config["relay"])
    try:
        relay.set(False)
        print("Relay OFF command sent")
    finally:
        relay.close()
    return 0


def _toml_quote(value: str) -> str:
    return json.dumps(value)


def command_setup(path: Path) -> int:
    print("MyAWOS Lite setup (transmission remains disabled)")
    station = input("Station identifier [54T]: ").strip() or "54T"
    while True:
        raw_frequency = input("Radio frequency MHz [122.700]: ").strip() or "122.700"
        try:
            frequency = float(raw_frequency)
            if not 118.0 <= frequency <= 136.975:
                raise ValueError
            break
        except ValueError:
            print("Enter an aviation COM frequency from 118.000 through 136.975 MHz.")
    relay = find_relay_port("auto") or "auto"
    detected_audio = detect_audio_device()
    audio = input(f"ALSA playback device [{detected_audio}]: ").strip() or detected_audio
    choices = {"weatherlink_live", "ecowitt_cloud", "sample"}
    while True:
        source = input("Weather source: weatherlink_live, ecowitt_cloud, or sample [weatherlink_live]: ").strip() or "weatherlink_live"
        if source in choices:
            break
        print("Choose weatherlink_live, ecowitt_cloud, or sample.")
    host = ""
    application_key = ""
    api_key = ""
    mac = ""
    if source == "weatherlink_live":
        host = input("WeatherLink Live IP address: ").strip()
    elif source == "ecowitt_cloud":
        application_key = input("Ecowitt application key: ").strip()
        api_key = input("Ecowitt API key: ").strip()
        mac = input("Ecowitt station MAC address: ").strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f'''[station]
identifier = {_toml_quote(station)}

[radio]
frequency_mhz = {frequency:.3f}
required_clicks = 5
click_window_seconds = 4.0
cooldown_seconds = 30

[receiver]
type = "airspy"
serial = "auto"
sample_rate = 2500000
chunk_bytes = 8192
calibration_samples = 700
threshold_on_ratio = 4.0
threshold_off_ratio = 2.5
min_click_gap_seconds = 0.20
min_quiet_time_seconds = 0.12
restart_delay_seconds = 0.5

[relay]
port = {_toml_quote(relay)}
baud = 9600
on_command_hex = "A0 01 01 A2"
off_command_hex = "A0 01 00 A1"

[transmitter]
enabled = false
audio_device = {_toml_quote(audio)}
ptt_lead_seconds = 0.5
ptt_tail_seconds = 0.3
max_seconds = 60

[weather]
type = {_toml_quote(source)}
host = {_toml_quote(host)}
port = 80
timeout_seconds = 5
refresh_seconds = 60
application_key = {_toml_quote(application_key)}
api_key = {_toml_quote(api_key)}
mac = {_toml_quote(mac)}
sample_file = "/usr/share/doc/myawos-lite/examples/sample-weather.json"

[paths]
state_directory = "/var/lib/myawos-lite"
media_directory = "/usr/share/myawos-lite/media"
'''
    path.write_text(content, encoding="utf-8")
    try:
        os.chown(path, -1, grp.getgrnam("myawos").gr_gid)
        os.chmod(path, 0o640)
    except KeyError:
        os.chmod(path, 0o600)
    print(f"Wrote {path}. Run 'myawos-lite --config {path} doctor' next.")
    return 0


def command_set_transmit(path: Path, enabled: bool, confirmed: bool = False) -> int:
    if enabled and not confirmed:
        print("Refusing to enable RF. Rerun with --confirm after completing the commissioning checklist.", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    replacement = f"enabled = {'true' if enabled else 'false'}"
    updated, count = re.subn(r"(?m)^enabled\s*=\s*(?:true|false)\s*$", replacement, text, count=1)
    if count != 1:
        raise ValueError("Could not find transmitter enabled setting")
    temporary = path.with_suffix(path.suffix + ".tmp")
    original = path.stat()
    temporary.write_text(updated, encoding="utf-8")
    os.chown(temporary, original.st_uid, original.st_gid)
    os.chmod(temporary, original.st_mode & 0o777)
    os.replace(temporary, path)
    action = "enabled" if enabled else "disabled"
    print(f"Automatic transmission {action}. Restart with: sudo systemctl restart myawos-lite")
    return 0


def command_status() -> int:
    return subprocess.run(["systemctl", "status", "myawos-lite", "--no-pager"], check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(prog="myawos-lite")
    parser.add_argument("--config", help=f"configuration file (default: {DEFAULT_CONFIG})")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="run the click detector and weather service")
    commands.add_parser("doctor", help="check hardware, software, and weather access")
    commands.add_parser("devices", help="list Airspy, serial relay, and audio devices")
    commands.add_parser("generate", help="fetch weather and generate current.wav")
    commands.add_parser("play-audio", help="play current.wav without keying PTT")
    commands.add_parser("relay-off", help="send only the fail-safe relay OFF command")
    commands.add_parser("setup", help="write a new transmit-disabled configuration")
    enable = commands.add_parser("enable-transmit", help="enable automatic RF after commissioning")
    enable.add_argument("--confirm", action="store_true", help="confirm wiring, authorization and RF checks are complete")
    commands.add_parser("disable-transmit", help="disable automatic RF")
    commands.add_parser("status", help="show the system service status")
    args = parser.parse_args()
    path = _config_path(args.config)
    if args.command == "setup":
        return command_setup(path)
    if args.command == "devices":
        return command_devices()
    if args.command == "enable-transmit":
        return command_set_transmit(path, True, args.confirm)
    if args.command == "disable-transmit":
        return command_set_transmit(path, False)
    if args.command == "status":
        return command_status()
    config = load_config(path)
    if args.command == "run":
        run(config)
        return 0
    if args.command == "doctor":
        return command_doctor(config)
    if args.command == "generate":
        return command_generate(config)
    if args.command == "play-audio":
        return command_play(config)
    if args.command == "relay-off":
        return command_relay_off(config)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
