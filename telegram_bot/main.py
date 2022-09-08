import os
from loguru import logger
from aiogram import Bot, Dispatcher, executor
from telegram_bot.handlers import register_user_handlers


async def __on_start_up(dp: Dispatcher):
    logger.info('Bot starts')
    register_user_handlers(dp)


def start_telegram_bot() -> None:
    bot = Bot(token=os.environ.get('TOKEN'))
    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
