from log_analyzer.src.log_analyzer.models.log_entry import LogEntry


def parse_log_entries(lines: str):
    for line in lines:
        entry = LogEntry.from_file_line(line)
        if entry:
            yield entry