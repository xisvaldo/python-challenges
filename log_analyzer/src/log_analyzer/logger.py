import logging
from logging import Formatter, FileHandler

def configure_logger():
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    info_log_handler = _create_info_log(formatter)
    error_log_handler = _create_error_log(formatter)
    logger.addHandler(info_log_handler)
    logger.addHandler(error_log_handler)

def _create_info_log(formatter: Formatter) -> FileHandler:
    return _create_handler(formatter=formatter, log_level=logging.INFO, file_name="info.log")

def _create_error_log(formatter: Formatter) -> FileHandler:
    return _create_handler(formatter=formatter, log_level=logging.ERROR, file_name="error.log")

def _create_handler(formatter: Formatter, log_level: int | str, file_name: str) -> FileHandler:
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    return file_handler