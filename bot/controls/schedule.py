import asyncio

import aiojobs
from loguru import logger

from bot.database import delete_outdated_concerts
from bot.parsing.controller import create_concerts


async def check_concerts() -> None:
    logger.info("Schedule check concerts")
    time_interval = 8 * 60 * 60
    while True:
        await create_concerts()
        delete_outdated_concerts()
        await asyncio.sleep(time_interval)


async def start_schedule() -> None:
    scheduler = aiojobs.Scheduler()
    await scheduler.spawn(check_concerts())
