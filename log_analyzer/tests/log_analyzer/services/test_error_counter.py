import unittest

from log_analyzer.src.log_analyzer.models.log_entry import LogEntry
from log_analyzer.src.log_analyzer.services.error_counter import count_errors_per_ip


class TestErrorCounter(unittest.TestCase):

    def setUp(self):
        self.public_ip = "192.168.1.1"
        self.log_entries = [
            LogEntry(timestamp="2026-01-01 10:00:00", ip=self.public_ip, method="GET", endpoint="/home",
                     status_code=200),
            LogEntry(timestamp="2026-01-01 10:01:00", ip=self.public_ip, method="POST", endpoint="/login",
                     status_code=401),
            LogEntry(timestamp="2026-01-01 10:02:00", ip=self.public_ip, method="GET", endpoint="/dashboard",
                     status_code=500),
            LogEntry(timestamp="2026-01-01 10:03:00", ip="8.8.8.8", method="GET", endpoint="/home", status_code=200),
            LogEntry(timestamp="2026-01-01 10:04:00", ip="8.8.8.8", method="GET", endpoint="/admin", status_code=403),
            LogEntry(timestamp="2026-01-01 10:05:00", ip="8.8.8.8", method="GET", endpoint="/home", status_code=404),
        ]

    def test_counts_only_errors_for_public_ip(self):
        count = count_errors_per_ip(log_entries=self.log_entries, public_ip=self.public_ip)
        self.assertEqual(count, 2)

    def test_ignores_non_error_status_codes(self):
        log_entries = [LogEntry("2026-01-01 10:00:00", self.public_ip, "GET", "/home", 200)]
        result = count_errors_per_ip(log_entries=log_entries, public_ip=self.public_ip)
        self.assertEqual(result, 0)

    def test_ignores_other_ips(self):
        log_entries = [LogEntry("2026-01-01 10:00:00", "8.8.8.8", "GET", "/home", 500)]
        result = count_errors_per_ip(log_entries=log_entries, public_ip=self.public_ip)
        self.assertEqual(result, 0)

    def test_empty_entries(self):
        result = count_errors_per_ip(log_entries=[], public_ip=self.public_ip)
        self.assertEqual(result, 0)

    def test_no_errors_found_for_public_ip(self):
        log_entries = [LogEntry("2026-01-01 10:00:00", self.public_ip, "GET", "/home", 200)]
        result = count_errors_per_ip(log_entries=log_entries, public_ip=self.public_ip)
        self.assertEqual(result, 0)
