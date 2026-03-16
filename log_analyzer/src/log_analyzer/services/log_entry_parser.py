import logging
from typing import Iterable, Generator

from log_analyzer.src.log_analyzer.models.log_entry import LogEntry


def parse_log_entries(lines: Iterable[str]) -> Generator[LogEntry, None, None]:
    for line_number, line in enumerate(lines, start=1):
        try:
            log_entry = LogEntry.from_file_line(line)
            yield log_entry

        except Exception as exception:
            logging.error(f"Failed to parse line {line}. Error: {exception}.", exc_info=True)
