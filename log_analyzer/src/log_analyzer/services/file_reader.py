import logging
from pathlib import Path
from typing import Generator, Union


def read_logs(path: Union[str, Path]) -> Generator[str, None, None]:
    logging.info(f"Reading logs from {path}.")

    try:
        with open(path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                yield line
    except FileNotFoundError:
        logging.error(f"File not found: {path}.")
    except IOError as exception:
        logging.error(f"Error while reading file {path}: {exception}.")
