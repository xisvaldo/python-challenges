import unittest

from log_analyzer.src.log_analyzer.models.log_entry import LogEntry


class TestsLogEntry(unittest.TestCase):

    def test_valid_log_entry(self):
        entry = LogEntry(
            timestamp="2026-03-17 15:25:08",
            ip="192.168.1.1",
            method="GET",
            endpoint="/home",
            status_code=200
        )
        self.assertEqual(entry.ip, "192.168.1.1")

    def test_invalid_timestamp_month(self):
        with self.assertRaises(ValueError):
            LogEntry(
                timestamp="2026-99-17 15:25:08",
                ip="192.168.1.1",
                method="GET",
                endpoint="/home",
                status_code=200
            )

    def test_invalid_timestamp_day(self):
        with self.assertRaises(ValueError):
            LogEntry(
                timestamp="2026-02-31 15:25:08",
                ip="192.168.1.1",
                method="GET",
                endpoint="/home",
                status_code=200
            )

    def test_invalid_ip_format(self):
        with self.assertRaises(ValueError):
            LogEntry(
                timestamp="2026-03-17 15:25:08",
                ip="192.999.1.1",
                method="GET",
                endpoint="/home",
                status_code=200
            )

    def test_invalid_http_method(self):
        with self.assertRaises(ValueError):
            LogEntry(
                timestamp="2026-03-17 15:25:08",
                ip="192.168.1.1",
                method="INVALID",
                endpoint="/home",
                status_code=200
            )

    def test_invalid_endpoint(self):
        with self.assertRaises(ValueError):
            LogEntry(
                timestamp="2026-03-17 15:25:08",
                ip="192.168.1.1",
                method="GET",
                endpoint="home",
                status_code=200
            )

    def test_invalid_status_code(self):
        with self.assertRaises(ValueError):
            LogEntry(
                timestamp="2026-03-17 15:25:08",
                ip="192.168.1.1",
                method="GET",
                endpoint="/home",
                status_code=888
            )

    def test_from_file_line_valid(self):
        line = "2026-03-17 15:25:08 | 192.168.1.1 | GET /home | 200"
        entry = LogEntry.from_file_line(line)
        self.assertEqual(entry.timestamp, "2026-03-17 15:25:08")
        self.assertEqual(entry.ip, "192.168.1.1")
        self.assertEqual(entry.method, "GET")
        self.assertEqual(entry.endpoint, "/home")
        self.assertEqual(entry.status_code, 200)

    def test_from_file_line_invalid(self):
        line = "some invalid line"
        with self.assertRaises(IOError):
            LogEntry.from_file_line(line)

    def test_from_file_line_invalid_method_endpoint_format(self):
        line = "2026-03-17 15:25:08 | 192.168.1.1 | GET/INVALID | 200"
        with self.assertRaises(IOError):
            LogEntry.from_file_line(line)

    def test_from_file_line_invalid_status_code(self):
        line = "2026-03-17 15:25:08 | 192.168.1.1 | GET /home | invalid"
        with self.assertRaises(IOError):
            LogEntry.from_file_line(line)


if __name__ == '__main__':
    unittest.main()
