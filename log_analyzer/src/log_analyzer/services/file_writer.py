import csv
import logging
from typing import Iterable


def write_csv_results(log_entries: Iterable, output_path: str):
    logging.info(f"Writing results to {output_path}.")

    try:
        with open(output_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["ip", "status_code"])
            writer.writeheader()

            for log_entry in log_entries:
                writer.writerow({"ip": log_entry.ip, "status_code": log_entry.status_code})

        logging.info(f"Results written to {output_path}.")

    except IOError as exception:
        logging.error(f"Failed to write to {output_path}: {exception}.")
