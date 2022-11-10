from datetime import date
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .kassir import Kassir
from bot.database.methods.get import get_all_concerts
from bot.database.methods.create import create_concert
from bot.database.methods.delete import delete_concert_by_id


async def update_database() -> None:
    check_out_dated()
    for item in await Kassir().get_data_from_all_urls():
        create_concert(item['name'], item['date'], item['price'], item['city'], item['link'])


def check_out_dated() -> None:
    today = date.today()
    for concert in get_all_concerts():
        if concert.date < today:
            delete_concert_by_id(concert.id)


def start_schedule() -> None:
    logger.info('Schedule started')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_database, 'interval', minutes=120, id='database')
    scheduler.start()
