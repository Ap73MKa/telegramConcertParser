import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from bot.controls import PathControl, start_schedule
from bot.database import register_models
from bot.handlers.controller import register_handlers
from bot.misc import Config
from bot.parsing import create_concerts, update_list_of_available_cities


def config_logs() -> None:
    if Config.DEBUG:
        log_path = PathControl.get("logs/{time}.log")
        logger.add(
            log_path,
            format="{time} {level} {message}",
            rotation="10:00",
            compression="zip",
            retention="3 days",
        )


async def on_start_up(dp: Dispatcher) -> None:
    logger.info("Bot starts")
    config_logs()
    register_models()
    register_handlers(dp)
    await update_list_of_available_cities()
    await create_concerts()
    start_schedule()


async def main() -> None:
    bot = Bot(token=Config.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    await on_start_up(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
