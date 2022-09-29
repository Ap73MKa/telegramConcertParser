from loguru import logger
from bot import start_telegram_bot
from bot.misc.path import PathManager


def main():
    log_path = PathManager.get('logs/{time}.log')
    logger.add(log_path, format="{time} {level} {message}", rotation="10:00", compression="zip", retention="3 days")
    start_telegram_bot()


if __name__ == '__main__':
    main()
