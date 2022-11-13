from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers import register_user_handlers
from bot.database import register_models, clean_outdated_concerts
from bot.modules import Config, set_language, ThrottlingMiddleware, PathManager, Schedule
from bot.parsing import create_concerts


async def on_start_up(dp: Dispatcher) -> None:
    logger.info('Bot starts')
    register_models()
    register_user_handlers(dp)
    set_language()
    scheduler = Schedule([create_concerts, clean_outdated_concerts])
    scheduler.start()


def start_telegram_bot() -> None:
    bot = Bot(token=Config.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)


if __name__ == '__main__':
    log_path = PathManager.get('logs/{time}.log')
    logger.add(log_path, format="{time} {level} {message}", rotation="10:00", compression="zip", retention="3 days")
    start_telegram_bot()
