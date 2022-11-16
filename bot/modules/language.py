from locale import setlocale, LC_ALL
from loguru import logger


def set_language() -> None:
    setlocale(LC_ALL, ('ru_RU', 'UTF-8'))
    logger.info('Locale changed to ru_RU.UTF-8')
