from bot.database import get_city_by_abb, add_many_concerts
from bot.database.city import add_many_cities
from .kassir import Kassir
from .kassir_cities import KassirCities


async def create_concerts():
    data = await Kassir().get_data_from_all_urls()
    for item in data:
        city = get_city_by_abb(item['city'])
        if not city:
            continue
        item['city'] = city
    add_many_concerts(data)


async def update_list_of_available_cities():
    add_many_cities(await KassirCities().get_data_from_all_urls())
