import argparse
import logging

from log_analyzer.src.log_analyzer.models.log_entry import LogEntry
from log_analyzer.src.log_analyzer.services.file_reader import read_logs
from log_analyzer.src.log_analyzer.services.file_writer import write_csv_results
from log_analyzer.src.log_analyzer.services.get_public_ip import get_public_ip
from log_analyzer.src.log_analyzer.utils.logger import configure_logging

RESULTS_FILE_NAME = "results.csv"


def main():
    configure_logging()

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input", help="Input log file")
    args = argument_parser.parse_args()

    logging.info("--- Starting Log Analyzer ---")

    parsed_log_entries = []
    client_error_count = 0
    client_ip = get_public_ip()

    lines = read_logs(args.input)

    parsed_log_entries = (
        log_entry
        for line in lines
        if (log_entry := parsed_log_entries(line)) is not None
    )

    for line in lines:
        log_entry = LogEntry.from_file_line(line)
        if log_entry:
            parsed_log_entries.append(log_entry)
            if log_entry.ip == client_ip and log_entry.status_code >= 400:
                client_error_count += 1

    write_csv_results(log_entries=parsed_log_entries, output_path=RESULTS_FILE_NAME)
    logging.info(f"Client error count: {client_error_count}.")
    logging.info("--- Finished Log Analyzer ---")


if __name__ == "__main__":
    main()
