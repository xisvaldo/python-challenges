import unittest
from pathlib import Path
from unittest.mock import patch

from log_analyzer.services.file_reader import read_logs


class TestFileReader(unittest.TestCase):

    def setUp(self):
        self.path = Path(__file__).parent.parent / "resources" / "log_entries_sample.txt"

    def test_read_valid_lines(self):
        lines = list(read_logs(self.path.as_posix()))
        self.assertTrue(len(lines) > 0)

    def test_skip_empty_lines(self):
        lines = list(read_logs(self.path.as_posix()))
        self.assertFalse("" in lines)

    def test_file_not_found(self):
        lines = list(read_logs("non_existent_file_path.txt"))
        self.assertEqual(len(lines), 0)

    def test_skip_lines_with_only_whitespace(self):
        lines = list(read_logs(self.path.as_posix()))
        for line in lines:
            self.assertTrue(line.strip() != "")

    def test_io_error_handling(self):
        with patch("builtins.open", side_effect=IOError("error")):
            lines = list(read_logs(self.path.as_posix()))
            self.assertEqual(lines, [])
