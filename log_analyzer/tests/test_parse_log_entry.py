from log_analyzer.src.log_analyzer.models.log_entry import LogEntry
import unittest

class ParseEntryLogTest(unittest.TestCase):

    def test_parsing_log_entry_is_successful(self):
        entry = LogEntry.from_file_line("2026-03-16 16:32:11 | 192.168.1.1 | GET /api/users | 200")
        assert entry.ip == "192.168.1.1"
        assert entry.status_code == 200

    def test_parsing_log_entry_raises_error_with_invalid_timestamp(self):
        try:
            LogEntry.from_file_line("2026-99-16 16:32:11 | 192.168.1.1 | GET /api/users | 200")
            assert False
        except ValueError:
            pass

    def test_parsing_log_entry_raises_error_with_invalid_ip(self):
        try :
            LogEntry.from_file_line("2026-03-16 16:32:11 | 192.168.1.1457 | GET /api/users | 200")
            assert False
        except ValueError:
            pass

    def test_parsing_log_entry_raises_error_with_invalid_method(self):
        try:
            LogEntry.from_file_line("2026-03-16 16:32:11 | 192.168.1.1457 | XOR /api/users | 200")
            assert False
        except ValueError:
            pass

    def test_parsing_log_entry_raises_error_with_invalid_endpoint(self):
        try:
            LogEntry.from_file_line("2026-03-16 16:32:11 | 192.168.1.1457 | GET api-users | 200")
            assert False
        except ValueError:
            pass

    def test_parsing_log_entry_raises_error_with_invalid_status_code(self):
        try:
            LogEntry.from_file_line("2026-03-16 16:32:11 | 192.168.1.1457 | GET /api/users | 2048")
            assert False
        except ValueError:
            pass

