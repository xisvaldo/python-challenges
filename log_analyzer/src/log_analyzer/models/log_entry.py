import re
from dataclasses import dataclass
from typing import Self

MIN_HTTP_STATUS_CODE = 100
MAX_HTTP_STATUS_CODE = 599


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
        timestamp_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        if not re.match(timestamp_pattern, self.timestamp):
            raise ValueError(f"Invalid timestamp: {self.timestamp}.")

    def _validate_ip(self):
        ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        ip_matching = re.match(ip_pattern, self.ip)
        if not ip_matching or not all(0 <= int(octet) <= 255 for octet in ip_matching.groups()):
            raise ValueError(f"Invalid ip: {self.ip}.")

    def _validate_method(self):
        methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "TRACE", "PATCH", "OPTIONS"}
        if self.method not in methods:
            raise ValueError(f"Invalid HTTP method: {self.method}.")

    def _validate_endpoint(self):
        if not self.endpoint.startswith("/"):
            raise ValueError(f"Invalid HTTP endpoint: {self.endpoint}.")

    def _validate_status_code(self):
        if not (MIN_HTTP_STATUS_CODE <= self.status_code <= MAX_HTTP_STATUS_CODE):
            raise ValueError(f"Invalid HTTP status code: {self.status_code}.")

    @classmethod
    def from_file_line(cls, line: str) -> Self:
        try:
            parts = [part.strip() for part in line.split("|")]
            if len(parts) != 4:
                raise ValueError(f"Invalid log entry: {line}.")

            method_endpoint = parts[2].split(" ")
            if len(method_endpoint) != 2:
                raise ValueError(f"Invalid method/endpoint format: {parts[2]}.")

            return LogEntry(
                timestamp=parts[0],
                ip=parts[1],
                method=method_endpoint[0],
                endpoint=method_endpoint[1],
                status_code=int(parts[3])
            )

        except Exception as exception:
            raise IOError(f"Failed to parse log entry: {line}. Exception: {exception}.")
