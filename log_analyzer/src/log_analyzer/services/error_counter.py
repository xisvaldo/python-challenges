from collections import Counter
from typing import Iterable

from log_analyzer.src.log_analyzer.models.log_entry import LogEntry


def count_errors_per_ip(entries: Iterable[LogEntry]) -> Counter:
    counter = Counter()
    for entry in entries:
        if entry.status_code >= 400:
            counter[entry.ip] += 1
    return counter
