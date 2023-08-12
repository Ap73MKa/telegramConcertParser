import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.bot.data_structure import TransferData
from src.bot.handlers import bot_commands, register_handlers
from src.config import configure
from src.database import (
    Database,
    create_async_engine,
    create_session_maker,
    process_scheme,
)


async def main() -> None:
    bot = Bot(token=configure.bot.token, parse_mode=ParseMode.HTML)

    # Dispatcher
    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp)
    await bot.set_my_commands(bot_commands)

    # Database
    url = configure.db.build_connection_str()
    engine = create_async_engine(url)
    session_maker = create_session_maker(engine)
    await process_scheme(engine)

    # Logs
    if configure.debug:
        log_path = Path().parent.parent / "logs" / "{time}.log"
        logger.add(
            log_path,
            format="{time} {level} {message}",
            rotation="10:00",
            compression="zip",
            retention="3 days",
        )

    # Parser
    async with session_maker() as session:
        db = Database(session)
        # await parse_city_list(db)
        # await parse_concerts(db)
        await db.concert.delete_outdated()
        await session.commit()
        # await start_parser_schedule(db)

    logger.info("Bot starts")
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(pool=session_maker),  # type: ignore
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
