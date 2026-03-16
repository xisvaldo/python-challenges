from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: str
    ip: str
    method: str
    endpoint: str
    status_code: int

    def from_file_line(self, line: str) -> LogEntry | None:
        try:
           parts = [part.strip() for part in line.split("|")]
           method_endpoint = parts[2].split(" ")
           return LogEntry(parts[0], parts[1], method_endpoint[0], method_endpoint[1], int(parts[4]))
        except Exception:
            return None