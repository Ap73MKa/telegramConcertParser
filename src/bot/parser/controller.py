from bot.parser.kassir_api import KassirApi
from bot.parser.kassir_cities import KassirCitiesGroupParser
from database.database import Database
from loguru import logger

from src.config import configure


async def parse_api(db: Database) -> None:
    cities = await db.city.get_many()
    domains = [f"{city.abb}.{configure.bot.kassir_site}" for city in cities]
    city_abb_to_id = {city.abb: city.id for city in cities}
    parser = KassirApi(domains)
    data = await parser.get_data_from_api()

    if not data:
        logger.warning("Parsing concerts - no concerts found")
        return
    dict_data = [
        {
            "name": item.name,
            "concert_date": item.date,
            "price": item.price,
            "link": item.link,
            "city_id": city_abb_to_id[item.city_abb],
        }
        for item in data
    ]

    await db.concert.insert(dict_data)


async def parse_city_list(db: Database) -> None:
    parser = KassirCitiesGroupParser()
    parsed_data = await parser.get_data_from_all_urls()
    if not parsed_data:
        logger.warning("Parsing city list - no cities found")
        return
    await db.city.insert(parsed_data)
    logger.info("Parsing city list - completed")
