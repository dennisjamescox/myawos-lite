from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class WeatherObservation:
    observed_at: datetime
    wind_direction_deg: int
    wind_speed_kt: int
    wind_gust_kt: int
    altimeter_inhg: float
    temperature_c: int
    dewpoint_c: int

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["observed_at"] = self.observed_at.astimezone(timezone.utc).isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WeatherObservation":
        return cls(
            observed_at=datetime.fromisoformat(str(data["observed_at"])),
            wind_direction_deg=int(data["wind_direction_deg"]),
            wind_speed_kt=int(data["wind_speed_kt"]),
            wind_gust_kt=int(data["wind_gust_kt"]),
            altimeter_inhg=float(data["altimeter_inhg"]),
            temperature_c=int(data["temperature_c"]),
            dewpoint_c=int(data["dewpoint_c"]),
        )
