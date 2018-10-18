import unittest
from Dashboard.report import get_psi_report, get_dengue_report, get_weather_report, get_incident_report, send_report


class TestReport(unittest.TestCase):
    def test_get_psi_report(self):
        self.assertIsNotNone(get_psi_report())

    def test_get_dengue_report(self):
        self.assertIsNotNone(get_dengue_report())

    def test_get_weather_report(self):
        self.assertIsNotNone(get_weather_report())
        self.assertIsNotNone(get_incident_report())

    def test_send_report(self):
        self.assertTrue(send_report())


if __name__ == '__main__':
    unittest.main()
