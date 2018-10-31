import unittest
from Dashboard.report import get_psi_report, get_dengue_report, get_weather_report, get_incident_report, send_report, parse_table, get_latest_report


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

    def test_parse_table(self):
        latest_report = get_latest_report(1)
        self.assertIsNotNone(parse_table(latest_report[0], id='dengue'))
        self.assertIsNotNone(parse_table(latest_report[0], id='psi'))
        self.assertIsNotNone(parse_table(latest_report[0], id='weather'))
        self.assertIsNotNone(parse_table(latest_report[0], id='incident'))


if __name__ == '__main__':
    unittest.main()
