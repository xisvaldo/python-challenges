import argparse
import logging

from log_analyzer.src.log_analyzer.services.error_counter import count_errors_per_ip
from log_analyzer.src.log_analyzer.services.file_reader import read_logs
from log_analyzer.src.log_analyzer.services.file_writer import write_csv_results
from log_analyzer.src.log_analyzer.services.get_public_ip import get_public_ip
from log_analyzer.src.log_analyzer.services.log_entry_parser import parse_log_entries
from log_analyzer.src.log_analyzer.utils.logger import configure_logging

RESULTS_FILE_NAME = "results.csv"


def main(input_file: str):
    configure_logging()

    logging.info("--- Starting Log Analyzer ---")

    client_ip = get_public_ip()
    lines = read_logs(input_file)
    parsed_log_entries = list(parse_log_entries(lines))
    client_error_count = count_errors_per_ip(log_entries=parsed_log_entries, public_ip=client_ip)

    write_csv_results(log_entries=parsed_log_entries, output_path=RESULTS_FILE_NAME)
    logging.info(f"Client error count: {client_error_count}.")
    logging.info("--- Finished Log Analyzer ---")


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input_file", help="Input log file.")
    argument_parser.add_argument("--generate-sample", action="store_true", help="Generate a sample log file.")
    argument_parser.add_argument("--sample_size", default=100_000, help="Number of entries in the sample log file.")
    args = argument_parser.parse_args()

    main(args.input_file)
