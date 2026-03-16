import argparse
from email import parser

from log_analyzer.src.log_analyzer.services.file_reader import read_logs
from log_analyzer.src.log_analyzer.services.file_writer import write_results
from log_analyzer.src.log_analyzer.services.get_public_ip import get_public_ip
from log_analyzer.src.log_analyzer.services.log_entry_parser import parse_log_entries
from log_analyzer.src.log_analyzer.utils.logger import Logger

RESULTS_FILE_NAME = "results.csv"

def main():
    logger = Logger()
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input", help="Input log file")
    args = parser.parse_args()

    lines = read_logs(args.input)
    parsed_log_entries = parse_log_entries(lines)
    write_results(entries=parsed_log_entries, output_path=RESULTS_FILE_NAME)
    client_ip = get_public_ip()

if __name__ == "__main__":
    main()