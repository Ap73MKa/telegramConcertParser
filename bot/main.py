from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.handlers import register_user_handlers
from bot.misc import EnvKeys
from bot.database.models import register_models


async def __on_start_up(dp: Dispatcher):
    logger.info('Bot starts')
    register_models()
    register_user_handlers(dp)


def start_telegram_bot() -> None:
    bot = Bot(token=EnvKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
