import tempfile
import unittest
from pathlib import Path

from myawos_lite.cli import command_set_transmit


class CliTests(unittest.TestCase):
    def test_enable_requires_confirmation_and_preserves_other_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "config.toml"
            config.write_text('[transmitter]\nenabled = false\naudio_device = "default"\n', encoding="utf-8")
            self.assertEqual(command_set_transmit(config, True, False), 2)
            self.assertIn("enabled = false", config.read_text())
            self.assertEqual(command_set_transmit(config, True, True), 0)
            contents = config.read_text()
            self.assertIn("enabled = true", contents)
            self.assertIn('audio_device = "default"', contents)


if __name__ == "__main__":
    unittest.main()
