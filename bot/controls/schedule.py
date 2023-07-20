from time import sleep
from threading import Thread
from asyncio import run
from loguru import logger

from bot.parsing.controller import create_concerts
from bot.database import delete_outdated_concerts


async def __func() -> None:
    logger.info("Schedule started")
    hours = 8 * 60 * 60
    while True:
        sleep(hours)
        await create_concerts()
        delete_outdated_concerts()


def start_schedule() -> None:
    thread = Thread(target=run, args=(__func(),))
    thread.start()
