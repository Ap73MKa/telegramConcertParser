from loguru import logger

from bot.database import (
    get_city_by_abb_or_none,
    insert_many_cities,
    insert_many_concerts,
)

from .kassir import KassirParser
from .kassir_cities import KassirCitiesParser


async def create_concerts() -> None:
    data = await KassirParser().get_data_from_all_urls()
    if not data:
        logger.warning("Parsing concerts - no concerts found")
        return
    for item in data:
        if city := get_city_by_abb_or_none(item["city"]):
            item["city"] = city
    insert_many_concerts(data)
    logger.info("Parsing concerts - completed")


async def update_list_of_available_cities() -> None:
    cities = await KassirCitiesParser().get_data_from_all_urls()
    if not cities:
        logger.warning("Parsing city list - no cities found")
        return
    insert_many_cities(cities)
    logger.info("Parsing city list - completed")
