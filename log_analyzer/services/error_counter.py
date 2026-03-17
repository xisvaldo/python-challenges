from typing import Iterable

from log_analyzer.models.log_entry import LogEntry

HTTP_ERROR_STATUS_CODE_RANGE = 400


def count_errors_per_ip(log_entries: Iterable[LogEntry], public_ip: str) -> int:
    counter = 0
    for entry in log_entries:
        if entry.status_code >= HTTP_ERROR_STATUS_CODE_RANGE and entry.ip == public_ip:
            counter += 1
    return counter
