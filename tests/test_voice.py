import json
import tempfile
import unittest
import wave
from datetime import datetime, timezone
from pathlib import Path

from myawos_lite.models import WeatherObservation
from myawos_lite.voice import announcement_tokens, build_announcement


ROOT = Path(__file__).parents[1]


class VoiceTests(unittest.TestCase):
    def observation(self):
        return WeatherObservation(
            datetime(2026, 9, 27, 14, 5, tzinfo=timezone.utc),
            170,
            8,
            13,
            29.92,
            -4,
            -8,
        )

    def test_tokens_include_padded_direction_altimeter_and_minus(self):
        tokens = announcement_tokens(self.observation())
        self.assertIn("gusts", tokens)
        self.assertEqual(tokens[tokens.index("wind") + 1 : tokens.index("at")], ["1", "7", "0"])
        self.assertIn("minus", tokens)
        altimeter = tokens.index("altimeter")
        self.assertEqual(tokens[altimeter + 1 : altimeter + 5], ["2", "9", "9", "2"])

    def test_builds_valid_wave_atomically(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "current.wav"
            build_announcement(self.observation(), ROOT / "media", output)
            with wave.open(str(output), "rb") as audio:
                self.assertEqual(audio.getframerate(), 44100)
                self.assertEqual(audio.getnchannels(), 2)
                self.assertGreater(audio.getnframes(), 1000)


if __name__ == "__main__":
    unittest.main()
