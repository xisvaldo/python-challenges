import logging
import sys
from logging import FileHandler
from pathlib import Path
from types import TracebackType
from typing import Type

INFO_LOG_FILE_NAME = "info.log"
ERROR_LOG_FILE_NAME = "error.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGS_DIRECTORY = Path(__file__).parent.parent / "logs"
LOGS_DIRECTORY.mkdir(parents=True, exist_ok=True)


def configure_logging() -> None:
    print("CONFIGURING LOGGER...")
    logger = logging.getLogger()
    logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    # Here we could also find a way to map CRITICAL to ERROR handler and WARNING to INFO handler
    info_log_handler = _create_info_log()
    error_log_handler = _create_error_log()
    logger.addHandler(info_log_handler)
    logger.addHandler(error_log_handler)
    
    def handle_exceptions(
            exception_type: Type[BaseException],
            exception_value: BaseException,
            traceback_object: TracebackType) -> None:
        if issubclass(exception_type, KeyboardInterrupt):
            sys.__excepthook__(exception_type, exception_value, traceback_object)
            return

        logging.error(msg="Uncaught exception", exc_info=(exception_type, exception_value, traceback_object))

    sys.excepthook = handle_exceptions


def _create_info_log() -> FileHandler:
    return _create_handler(log_level=logging.INFO, file_name=INFO_LOG_FILE_NAME)


def _create_error_log() -> FileHandler:
    return _create_handler(log_level=logging.ERROR, file_name=ERROR_LOG_FILE_NAME)


def _create_handler(log_level: int | str, file_name: str) -> FileHandler:
    file_path = LOGS_DIRECTORY / file_name
    file_handler = logging.FileHandler(file_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler.setLevel(log_level)
    file_handler.addFilter(lambda record: record.levelno == log_level)
    return file_handler
