import csv
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from log_analyzer.models.log_entry import LogEntry
from log_analyzer.services.file_writer import write_csv_results


class TestFileWriter(unittest.TestCase):

    def setUp(self):
        self.output_path = Path(__file__).parent.parent / "results.csv"
        self.log_entries = [
            LogEntry(timestamp="2026-01-01 10:00:00", ip="192.168.1.1", method="GET", endpoint="/home",
                     status_code=200),
            LogEntry(timestamp="2026-01-01 10:01:00", ip="192.168.1.1", method="POST", endpoint="/login",
                     status_code=401),
            LogEntry(timestamp="2026-01-01 10:02:00", ip="8.8.8.8", method="GET", endpoint="/admin", status_code=500),
        ]

    def tearDown(self):
        if self.output_path.exists():
            os.remove(self.output_path)

    def test_writes_csv_file(self):
        write_csv_results(log_entries=self.log_entries, output_path=self.output_path)
        self.assertTrue(self.output_path.exists())

    def test_writes_headers_correctly(self):
        write_csv_results(log_entries=self.log_entries, output_path=self.output_path)
        with (open(self.output_path, "r")) as file:
            reader = csv.reader(file)
            header = next(reader)
        self.assertEqual(header, ["ip", "status_code"])

    def test_writes_all_rows(self):
        write_csv_results(log_entries=self.log_entries, output_path=self.output_path)
        with (open(self.output_path, "r")) as file:
            reader = list(csv.DictReader(file))
        self.assertEqual(len(reader), len(self.log_entries))

    def test_writes_content_correctly(self):
        write_csv_results(log_entries=self.log_entries, output_path=self.output_path)
        with (open(self.output_path, "r")) as file:
            reader = list(csv.DictReader(file))

        self.assertEqual(reader[0]["ip"], "192.168.1.1")
        self.assertEqual(reader[1]["ip"], "192.168.1.1")
        self.assertEqual(reader[2]["ip"], "8.8.8.8")
        self.assertEqual(reader[0]["status_code"], "200")
        self.assertEqual(reader[1]["status_code"], "401")
        self.assertEqual(reader[2]["status_code"], "500")

    def test_empty_entries_writes_only_header(self):
        write_csv_results(log_entries=[], output_path=self.output_path)
        with (open(self.output_path, "r")) as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 1)  # header

    def test_accepts_generator(self):
        def generator():
            for log_entry in self.log_entries:
                yield log_entry

        write_csv_results(log_entries=generator(), output_path=self.output_path)
        with (open(self.output_path, "r")) as file:
            reader = list(csv.DictReader(file))
        self.assertEqual(len(reader), len(self.log_entries))

    def test_io_error_handling(self):
        with patch("builtins.open", side_effect=IOError("error")):
            with self.assertLogs(level="ERROR") as log:
                write_csv_results(log_entries=self.log_entries, output_path="invalid_output.csv")

                self.assertTrue(any("Failed to write" in message for message in log.output))
