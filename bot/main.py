from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.handlers import register_user_handlers
from bot.database.models import register_models
from bot.misc import Config, start_schedule, set_language
from bot.misc.throttle import ThrottlingMiddleware


async def __on_start_up(dp: Dispatcher):
    logger.info('Bot starts')
    register_models()
    register_user_handlers(dp)
    set_language()
    start_schedule()


def start_telegram_bot() -> None:
    bot = Bot(token=Config.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
