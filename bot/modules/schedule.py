from time import sleep
from threading import Thread
from asyncio import run
from loguru import logger

from bot.database import clean_outdated_concerts
from bot.parsing import create_concerts


async def func() -> None:
    logger.info("Schedule started")
    hours = 8 * 60 * 60
    while True:
        sleep(hours)
        await create_concerts()
        clean_outdated_concerts()


def start_schedule() -> None:
    thread = Thread(target=run, args=(func(),))
    thread.start()
