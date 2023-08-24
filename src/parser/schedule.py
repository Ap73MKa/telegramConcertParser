import asyncio

import aiojobs
from database.database import Database
from loguru import logger
from parser.controller import parse_api
from sqlalchemy.ext.asyncio import async_sessionmaker


async def check_concerts(session_maker: async_sessionmaker) -> None:
    time_interval = 12 * 60 * 60
    while True:
        logger.info("Scheduler checks new concerts")
        async with session_maker() as session:
            db = Database(session)
            await parse_api(db)
            await db.concert.delete_outdated()
            await session.commit()
        await asyncio.sleep(time_interval)


async def start_parser_schedule(session_maker: async_sessionmaker) -> None:
    scheduler = aiojobs.Scheduler()
    await scheduler.spawn(check_concerts(session_maker))
