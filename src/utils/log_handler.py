import logging
import os

from src.utils.singleton import SingletonMetaClass
from config_path import LOG_DIR


class Logger(metaclass=SingletonMetaClass):

    def __init__(self, app_name, level=logging.DEBUG, log_file_name="work.log"):
        self._logger = logging.getLogger(app_name)
        self._logger.setLevel(level)
        file_name = os.path.join(LOG_DIR, log_file_name)

        _log_handler = logging.FileHandler(file_name)
        _log_handler.setLevel(logging.DEBUG)

        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s >>> [%(name)s]: %(message)s")
        _log_handler.setFormatter(formatter)
        _console_handler.setFormatter(formatter)

        self._logger.addHandler(_log_handler)
        self._logger.addHandler(_console_handler)

    def get_log(self):
        return self._logger


if __name__ == '__main__':
    t1 = Logger("ToolMu")
    t2 = Logger("ToolMu")

    assert t1 == t2
    logger = Logger("ToolMu").get_log()
    logger.error("[Logger1] Something Error!")

    logger2 = Logger("ToolMu").get_log()
    logger2.error("[Logger2] Something Error!")
    print("OK!")
