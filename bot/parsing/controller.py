from bot.database import create_concert
from bot.database.city_list import create_city, get_all_city
from .kassir import Kassir
from .kassir_cities import KassirCities


async def create_concerts():
    for item in await Kassir().get_data_from_all_urls():
        create_concert(item['name'], item['date'], item['price'], item['city'], item['link'])


async def update_cities():
    if not get_all_city():
        for item in await KassirCities().get_data_from_all_urls():
            create_city(abb=item['abb'], name=item['name'])
