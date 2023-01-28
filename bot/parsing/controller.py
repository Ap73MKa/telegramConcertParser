from loguru import logger

from bot.database import get_city_by_abb_or_none, insert_many_concerts, insert_many_cities
from .kassir import KassirParser
from .kassir_cities import KassirCitiesParser


async def create_concerts() -> None:
    logger.info('Updating concert list')
    data = await KassirParser().get_data_from_all_urls()
    for item in data:
        if city := get_city_by_abb_or_none(item['city']):
            item['city'] = city
    insert_many_concerts(data)
    logger.info('Updating concert list completed')


async def update_list_of_available_cities() -> None:
    cities = await KassirCities().get_data_from_all_urls()
    if not cities:
        logger.warning('No cities found')
        return
    insert_many_cities(cities)
    logger.info('Updating city list completed')

