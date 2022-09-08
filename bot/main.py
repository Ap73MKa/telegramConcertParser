from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
from aiogram import Bot, Dispatcher, executor
from bot.handlers import register_user_handlers
from bot.misc import EnvKeys


async def __on_start_up(dp: Dispatcher):
    logger.info('Bot starts')
    register_user_handlers(dp)


def start_telegram_bot() -> None:
    bot = Bot(token=EnvKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
