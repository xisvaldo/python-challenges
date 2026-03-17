import unittest
from unittest.mock import patch

from log_analyzer.src.log_analyzer.models.log_entry import LogEntry
from log_analyzer.src.log_analyzer.services.log_entry_parser import parse_log_entries


class TestLogEntryParser(unittest.TestCase):

    def setUp(self):
        self.valid_lines = [
            "2026-03-17 15:30:00 | 192.168.1.1 | GET /home | 200",
            "2026-03-17 15:31:00 | 8.8.8.8 | POST /login | 401"
        ]
        self.invalid_lines = [
            "",
            "2026-03-17 15:32:00 | 999.999.999.999 | GET /home | 200",
            "2026-03-17 15:33:00 | 192.168.1.1 | INVALID /home | 200",
            "malformed line without separators"
        ]

    def test_parse_valid_lines(self):
        log_entries = list(parse_log_entries(self.valid_lines))
        self.assertEqual(len(log_entries), len(self.valid_lines))
        self.assertIsInstance(log_entries[0], LogEntry)
        self.assertEqual(log_entries[0].ip, "192.168.1.1")
        self.assertEqual(log_entries[1].method, "POST")

    @patch("logging.error")
    def test_parse_invalid_lines_logs_error(self, mock_logging_error):
        list(parse_log_entries(self.invalid_lines))
        self.assertEqual(mock_logging_error.call_count, len(self.invalid_lines))

    def test_mixed_valid_invalid_lines(self):
        mixed_lines = self.valid_lines + self.invalid_lines
        log_entries = list(parse_log_entries(mixed_lines))
        self.assertEqual(len(log_entries), len(self.valid_lines))
        self.assertEqual(log_entries[0].ip, "192.168.1.1")
        self.assertEqual(log_entries[0].status_code, 200)

    @patch("logging.error")
    def test_empty_lines_input(self, mock_logging_error):
        log_entries = list(parse_log_entries([]))
        self.assertEqual(len(log_entries), 0)
        mock_logging_error.assert_not_called()
