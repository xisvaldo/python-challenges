import re
from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: str
    ip: str
    method: str
    endpoint: str
    status_code: int

    def __post_init__(self):
        self._validate_timestamp()
        self._validate_ip()
        self._validate_method()
        self._validate_endpoint()
        self._validate_status_code()

    def _validate_timestamp(self):
        timestamp_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"
        if not re.match(timestamp_pattern, self.timestamp):
            raise ValueError(f"Invalid timestamp: {self.timestamp}")

    def _validate_ip(self):
        ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        if not re.match(ip_pattern, self.ip):
            raise ValueError(f"Invalid ip: {self.ip}")

    def _validate_method(self):
        methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "TRACE", "PATCH", "OPTIONS"}
        if self.method not in methods:
            raise ValueError(f"Invalid HTTP method: {self.method}")

    def _validate_endpoint(self):
        if not self.endpoint.startswith("/"):
            raise ValueError(f"Invalid HTTP endpoint: {self.endpoint}")

    def _validate_status_code(self):
        status_code_pattern = r"^[0-9]{1,5}$"
        if not re.match(status_code_pattern, str(self.status_code)):
            raise ValueError(f"Invalid HTTP status code: {self.status_code}")

    @classmethod
    def from_file_line(cls, line: str) -> LogEntry | None:
        try:
           parts = [part.strip() for part in line.split("|")]
           method_endpoint = parts[2].split(" ")
           return LogEntry(parts[0], parts[1], method_endpoint[0], method_endpoint[1], int(parts[3]))
        except Exception:
            return None