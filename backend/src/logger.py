import logging
from logging.handlers import RotatingFileHandler

from logzero import logger


class MyCsvFormatter(logging.Formatter):
    def __init__(self) -> None:
        fmt = "%(asctime)s,%(levelname)s,%(message)s"
        super(MyCsvFormatter, self).__init__(fmt=fmt)

    def format(self, record) -> str:
        msg = record.getMessage()
        record.msg = msg.replace(",", " ")
        return super(MyCsvFormatter, self).format(record)


def setup_global_logger(file_path: str) -> None:

    file_handler = RotatingFileHandler(
        file_path, maxBytes=int(1e6), backupCount=5, delay=False
    )
    # TODO: Store as json
    formatter = logging.Formatter("%(asctime)s,%(levelname)s,%(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
