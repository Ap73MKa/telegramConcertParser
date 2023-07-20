from locale import setlocale, LC_ALL
from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.database import register_models
from bot.handlers import register_user_handlers
from bot.parsing import update_list_of_available_cities, create_concerts

from bot.misc import Config
from bot.middlewares import ThrottlingMiddleware
from bot.controls import PathControl, start_schedule


async def __on_start_up(dp: Dispatcher) -> None:
    logger.info("Bot starts")
    register_models()
    register_user_handlers(dp)
    setlocale(LC_ALL, ("ru_RU", "UTF-8"))
    await update_list_of_available_cities()
    await create_concerts()
    start_schedule()


def __start_telegram_bot() -> None:
    bot = Bot(token=Config.TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)


def __main() -> None:
    if Config.DEBUG:
        log_path = PathControl.get("bot/logs/{time}.log")
        logger.add(
            log_path,
            format="{time} {level} {message}",
            rotation="10:00",
            compression="zip",
            retention="3 days",
        )
    __start_telegram_bot()


if __name__ == "__main__":
    __main()
