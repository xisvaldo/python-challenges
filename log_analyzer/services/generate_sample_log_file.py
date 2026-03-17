import datetime
import logging
import random
from pathlib import Path

from log_analyzer.services.get_public_ip import get_public_ip


def generate_sample_log_file(max_lines: int = 100_000) -> str:
    public_ip = get_public_ip() or "192.168.1.100"
    other_ips = ["8.8.8.8", "1.1.1.1", "123.45.67.89"]
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    endpoints = ["/home", "/login", "/dashboard", "/admin"]
    status_codes = [200, 201, 400, 401, 403, 404, 500]

    current_time = datetime.datetime.now()
    sample_logs_file = Path(__file__).resolve().parent.parent / "outputs" / "sample_logs.txt"
    sample_logs_file.parent.mkdir(parents=True, exist_ok=True)

    with(open(sample_logs_file, "w", newline="", encoding="utf-8")) as file:
        for line in range(max_lines):
            current_time += datetime.timedelta(seconds=random.randint(1, 10))
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            ip = random.choice([public_ip] + other_ips * 2)
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            status = random.choice(status_codes)

            if line % 50 == 0:
                file.write(f"{timestamp} | {ip} | INVALID /invalid | 999\n")
            elif line % 37 == 0:
                file.write(f"{timestamp} | {ip} | {method} /invalid | abc\n")
            else:
                file.write(f"{timestamp} | {ip} | {method} {endpoint} | {status}\n")

    logging.info("Log analyzer will be executed using a generated sample log file.")
    return str(sample_logs_file)
