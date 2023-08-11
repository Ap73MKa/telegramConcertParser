from bot.parser.kassir import KassirParser
from bot.parser.kassir_cities import KassirCitiesParser
from database.database import Database
from loguru import logger

from src.config import configure


async def parse_concerts(db: Database) -> None:
    cities = await db.city.get_many()
    urls = [f"https://{city.abb}.{configure.bot.kassir_link}" for city in cities]
    parser = KassirParser(urls)
    data = await parser.get_data_from_all_urls()
    city_abb_to_id = {city.abb: city.id for city in cities}

    filtered_data = [{
        'name': item['name'],
        'concert_date': item['date'],
        'price': item['price'],
        'link': item['link'],
        'city_id': city_abb_to_id[item['city_abb']]
    } for item in data]

    if not data:
        logger.warning("Parsing concerts - no concerts found")
        return

    await db.concert.insert(filtered_data)
    logger.info("Parsing concerts - completed")


async def parse_city_list(db: Database) -> None:
    parser = KassirCitiesParser()
    parsed_data = await parser.get_data_from_all_urls()
    if not parsed_data:
        logger.warning("Parsing city list - no cities found")
        return
    await db.city.insert(parsed_data)
    logger.info("Parsing city list - completed")
