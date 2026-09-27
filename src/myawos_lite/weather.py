from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import WeatherObservation


MPH_TO_KT = 0.868976


def _get_json(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "MyAWOS-Lite/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"Weather station returned HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))


def _round_direction(value: float) -> int:
    return (round(float(value) / 10) * 10) % 360


def _f_to_c(value: float) -> int:
    return round((float(value) - 32.0) * 5.0 / 9.0)


def fetch_weatherlink_live(settings: dict[str, Any]) -> WeatherObservation:
    host = str(settings.get("host", "")).strip()
    if not host:
        raise ValueError("weather.host is required for weatherlink_live")
    url = f"http://{host}:{int(settings.get('port', 80))}/v1/current_conditions"
    payload = _get_json(url, float(settings.get("timeout_seconds", 5)))
    conditions = payload.get("data", {}).get("conditions", [])
    outdoor = next(
        (item for item in conditions if item.get("data_structure_type") == 1 and item.get("txid", 1) == 1),
        None,
    ) or next((item for item in conditions if item.get("data_structure_type") == 1), None)
    barometer = next((item for item in conditions if item.get("data_structure_type") == 3), None)
    if not outdoor or not barometer:
        raise ValueError("WeatherLink response lacks outdoor or barometer data")
    return WeatherObservation(
        observed_at=datetime.now(timezone.utc),
        wind_direction_deg=_round_direction(outdoor["wind_dir_scalar_avg_last_1_min"]),
        wind_speed_kt=round(float(outdoor["wind_speed_avg_last_1_min"]) * MPH_TO_KT),
        wind_gust_kt=round(float(outdoor["wind_speed_hi_last_2_min"]) * MPH_TO_KT),
        altimeter_inhg=round(float(barometer["bar_sea_level"]), 2),
        temperature_c=_f_to_c(outdoor["temp"]),
        dewpoint_c=_f_to_c(outdoor["dew_point"]),
    )


def fetch_ecowitt_cloud(settings: dict[str, Any]) -> WeatherObservation:
    required = ("application_key", "api_key", "mac")
    missing = [key for key in required if not str(settings.get(key, "")).strip()]
    if missing:
        raise ValueError(f"Ecowitt settings missing: {', '.join(missing)}")
    query = urllib.parse.urlencode(
        {
            "application_key": settings["application_key"],
            "api_key": settings["api_key"],
            "mac": settings["mac"],
            "call_back": "all",
        }
    )
    payload = _get_json(
        f"https://api.ecowitt.net/api/v3/device/real_time?{query}",
        float(settings.get("timeout_seconds", 15)),
    )
    data = payload["data"]
    wind = data["wind"]
    pressure = data["pressure"]
    outdoor = data["outdoor"]
    return WeatherObservation(
        observed_at=datetime.now(timezone.utc),
        wind_direction_deg=_round_direction(wind["wind_direction"]["value"]),
        wind_speed_kt=round(float(wind["wind_speed"]["value"]) * MPH_TO_KT),
        wind_gust_kt=round(float(wind.get("wind_gust", wind["wind_speed"])["value"]) * MPH_TO_KT),
        altimeter_inhg=round(float(pressure["relative"]["value"]), 2),
        temperature_c=_f_to_c(outdoor["temperature"]["value"]),
        dewpoint_c=_f_to_c(outdoor["dew_point"]["value"]),
    )


def fetch_sample(settings: dict[str, Any]) -> WeatherObservation:
    path = Path(str(settings.get("sample_file", "")))
    if not path.is_file():
        raise ValueError(f"Sample weather file not found: {path}")
    return WeatherObservation.from_dict(json.loads(path.read_text(encoding="utf-8")))


def fetch(config: dict[str, Any]) -> WeatherObservation:
    settings = config["weather"]
    source = str(settings.get("type", "weatherlink_live"))
    if source == "weatherlink_live":
        return fetch_weatherlink_live(settings)
    if source == "ecowitt_cloud":
        return fetch_ecowitt_cloud(settings)
    if source == "sample":
        return fetch_sample(settings)
    raise ValueError(f"Unsupported weather source: {source}")
