import logging
from logging import Formatter, FileHandler


INFO_LOG_FILE_NAME = "info.log"
ERROR_LOG_FILE_NAME = "error.log"

class Logger:
    logger: logging.Logger
    formatter: Formatter

    def __init__(self):
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        info_log_handler = self._create_info_log()
        error_log_handler = self._create_error_log()
        self.logger.addHandler(info_log_handler)
        self.logger.addHandler(error_log_handler)

    def _create_info_log(self) -> FileHandler:
        return self._create_handler(log_level=logging.INFO, file_name=INFO_LOG_FILE_NAME)

    def _create_error_log(self) -> FileHandler:
        return self._create_handler(log_level=logging.ERROR, file_name=ERROR_LOG_FILE_NAME)

    def _create_handler(self, log_level: int | str, file_name: str) -> FileHandler:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(log_level)
        return file_handler