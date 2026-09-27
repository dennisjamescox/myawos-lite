import json
import unittest
from unittest.mock import MagicMock, patch

from myawos_lite.weather import fetch_weatherlink_live


class WeatherTests(unittest.TestCase):
    @patch("myawos_lite.weather.urllib.request.urlopen")
    def test_weatherlink_live_mapping(self, urlopen):
        payload = {
            "data": {
                "conditions": [
                    {
                        "data_structure_type": 1,
                        "txid": 1,
                        "wind_dir_scalar_avg_last_1_min": 174,
                        "wind_speed_avg_last_1_min": 10,
                        "wind_speed_hi_last_2_min": 15,
                        "temp": 77,
                        "dew_point": 59,
                    },
                    {"data_structure_type": 3, "bar_sea_level": 29.92},
                ]
            }
        }
        response = MagicMock()
        response.status = 200
        response.read.return_value = json.dumps(payload).encode()
        response.__enter__.return_value = response
        urlopen.return_value = response

        observation = fetch_weatherlink_live({"host": "192.0.2.10", "port": 80, "timeout_seconds": 2})

        self.assertEqual(observation.wind_direction_deg, 170)
        self.assertEqual(observation.wind_speed_kt, 9)
        self.assertEqual(observation.wind_gust_kt, 13)
        self.assertEqual(observation.temperature_c, 25)
        self.assertEqual(observation.dewpoint_c, 15)
        self.assertEqual(observation.altimeter_inhg, 29.92)


if __name__ == "__main__":
    unittest.main()
