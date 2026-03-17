import csv
import logging
from pathlib import Path
from typing import Iterable

from log_analyzer.models.log_entry import LogEntry


def write_csv_results(log_entries: Iterable[LogEntry]):
    results_csv_file = Path(__file__).resolve().parent.parent / "outputs" / "results.csv"
    results_csv_file.parent.mkdir(parents=True, exist_ok=True)
    logging.info(f"Writing results to {results_csv_file}.")

    try:
        with open(results_csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["ip", "status_code"])
            writer.writeheader()

            for log_entry in log_entries:
                writer.writerow({"ip": log_entry.ip, "status_code": log_entry.status_code})

        logging.info(f"Results written to {results_csv_file}.")

    except IOError as exception:
        logging.error(f"Failed to write to {results_csv_file}: {exception}.")
