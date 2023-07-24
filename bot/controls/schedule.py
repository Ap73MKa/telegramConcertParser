from asyncio import run
from threading import Thread
from time import sleep

from loguru import logger

from bot.database import delete_outdated_concerts
from bot.parsing.controller import create_concerts


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
