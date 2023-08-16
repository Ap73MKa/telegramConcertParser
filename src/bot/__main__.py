import asyncio
import locale

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.parser.controller import parse_city_list
from bot.parser.schedule import start_parser_schedule
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.bot.data_structure import TransferData
from src.bot.handlers import bot_commands, register_handlers
from src.config import configure
from src.database import (
    Database,
    create_async_engine,
    create_session_maker,
    process_scheme,
)
from src.logs import set_up_configs


def set_localization() -> None:
    try:
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    finally:
        pass


async def set_up_parser(session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        db = Database(session)
        await parse_city_list(db)
        await session.commit()
    await start_parser_schedule(session_maker)


async def run_bot() -> None:
    if configure.debug:
        set_up_configs()
    set_localization()

    # Dispatcher
    bot = Bot(token=configure.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp)
    await bot.set_my_commands(bot_commands)
    logger.info("Bot starts")

    # Database
    url = configure.db.build_connection_str()
    engine = create_async_engine(url)
    session_maker = create_session_maker(engine)
    await process_scheme(engine)
    await set_up_parser(session_maker)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(pool=session_maker),  # type: ignore
    )


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
