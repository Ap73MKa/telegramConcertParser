import asyncio
import datetime

import aiojobs
from database.database import Database
from database.models import Concert
from loguru import logger


async def check_concerts(db: Database) -> None:
    logger.info("Schedule check concerts")
    time_interval = 8 * 60 * 60
    while True:
        # await parse_concerts(db)
        await db.concert.delete(Concert.concert_date < datetime.date.today())
        await asyncio.sleep(time_interval)


async def start_parser_schedule(db: Database) -> None:
    scheduler = aiojobs.Scheduler()
    await scheduler.spawn(check_concerts(db))
