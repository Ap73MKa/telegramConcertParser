from .kassir import Kassir

from bot.database import create_concert


async def create_concerts():
    for item in await Kassir().get_data_from_all_urls():
        create_concert(item['name'], item['date'], item['price'], item['city'], item['link'])
