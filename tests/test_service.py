import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from myawos_lite.service import WeatherWorker, weather_audio_for_transmission


class WeatherAudioSafetyTests(unittest.TestCase):
    def config(self, root: Path) -> dict:
        media = root / "media"
        state = root / "state"
        media.mkdir()
        state.mkdir()
        (media / "WeatherStation_no_weather_available_at_this_time.wav").write_bytes(b"outage")
        (state / "current.wav").write_bytes(b"weather")
        return {
            "weather": {"max_age_hours": 12},
            "paths": {"state_directory": str(state), "media_directory": str(media)},
        }

    def write_observed_at(self, config: dict, observed_at: datetime) -> None:
        path = Path(config["paths"]["state_directory"]) / "current-weather.json"
        path.write_text(json.dumps({"observed_at": observed_at.isoformat()}), encoding="utf-8")

    def test_fresh_weather_uses_current_announcement(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = self.config(Path(temporary))
            now = datetime(2026, 10, 16, 12, tzinfo=timezone.utc)
            self.write_observed_at(config, now - timedelta(hours=11, minutes=59))

            audio, unavailable = weather_audio_for_transmission(config, now)

            self.assertEqual(audio.name, "current.wav")
            self.assertFalse(unavailable)

    def test_weather_at_twelve_hours_uses_only_unavailable_announcement(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = self.config(Path(temporary))
            now = datetime(2026, 10, 16, 12, tzinfo=timezone.utc)
            self.write_observed_at(config, now - timedelta(hours=12))

            audio, unavailable = weather_audio_for_transmission(config, now)

            self.assertEqual(audio.name, "WeatherStation_no_weather_available_at_this_time.wav")
            self.assertTrue(unavailable)

    def test_missing_metadata_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = self.config(Path(temporary))

            audio, unavailable = weather_audio_for_transmission(config)

            self.assertEqual(audio.name, "WeatherStation_no_weather_available_at_this_time.wav")
            self.assertTrue(unavailable)

    @patch("myawos_lite.service.fetch", side_effect=ConnectionError("station unavailable"))
    def test_failed_refresh_cannot_make_old_weather_fresh(self, _fetch):
        with tempfile.TemporaryDirectory() as temporary:
            config = self.config(Path(temporary))
            now = datetime(2026, 10, 16, 12, tzinfo=timezone.utc)
            self.write_observed_at(config, now - timedelta(hours=13))

            with self.assertRaises(ConnectionError):
                WeatherWorker(config).refresh()
            audio, unavailable = weather_audio_for_transmission(config, now)

            self.assertEqual(audio.name, "WeatherStation_no_weather_available_at_this_time.wav")
            self.assertTrue(unavailable)


if __name__ == "__main__":
    unittest.main()
