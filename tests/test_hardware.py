import logging
import unittest

from myawos_lite.hardware import AirspyReceiver, ClickDetector


class Triggered(Exception):
    pass


class FakeReceiver:
    def __init__(self, levels):
        self.levels = iter(levels)

    def read_level(self):
        return next(self.levels)


class ClickDetectorTests(unittest.TestCase):
    def test_airspy_serial_uses_supported_argument(self):
        receiver = AirspyReceiver(
            {
                "radio": {"frequency_mhz": 122.7},
                "receiver": {"serial": "ABC123", "sample_rate": 2_500_000},
            }
        )
        self.assertIn("-s", receiver.command)
        self.assertNotIn("-d", receiver.command)

    def test_five_clicks_trigger_once(self):
        config = {
            "radio": {
                "required_clicks": 5,
                "click_window_seconds": 4,
                "cooldown_seconds": 30,
            },
            "receiver": {
                "calibration_samples": 5,
                "threshold_on_ratio": 4,
                "threshold_off_ratio": 2,
                "min_click_gap_seconds": 0,
                "min_quiet_time_seconds": 0,
            },
        }
        receiver = FakeReceiver([10] * 5 + [50, 10, 50, 10, 50, 10, 50, 10, 50])
        detector = ClickDetector(config, logging.getLogger("test"))

        with self.assertRaises(Triggered):
            detector.run(receiver, lambda: (_ for _ in ()).throw(Triggered()))


if __name__ == "__main__":
    unittest.main()
