import logging
from pathlib import Path

from loguru import logger


class PropagateHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name
        logger.opt(depth=1, exception=record.exc_info).log(level, record.getMessage())


def set_up_configs() -> None:
    log_path = Path().parent.parent / "logs" / "{time}.log"
    logger.add(
        log_path,
        format="{time} {level} {message}",
        rotation="10:00",
        compression="zip",
        retention="3 days",
    )
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.addHandler(PropagateHandler())
    sqlalchemy_logger.setLevel(logging.DEBUG)
