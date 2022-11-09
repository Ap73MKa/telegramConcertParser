from typing import NamedTuple
from asyncio import gather
from loguru import logger
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from bot.misc.config import Config
from bot.misc.reformat import get_cities, get_city_from_url, reformat_date, reformat_price
from bot.database.methods.create import create_concert
from bot.database.methods.get import get_all_concerts
from bot.database.methods.delete import delete_concert_by_id
from datetime import date


class CategoryId(NamedTuple):
    HUMOR = 4073
    HIP_HOP = 3007
    ELECTRONIC = 3008
    ROCK = 3002
    POP = 3003


def get_params() -> dict[str, list[int] | int]:
    return {
        'category[]': [CategoryId.HUMOR, CategoryId.ELECTRONIC, CategoryId.HIP_HOP,
                       CategoryId.ROCK, CategoryId.POP],
        'sort': 0,
        'c': 30
    }


def get_header() -> dict[str, str]:
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def fetch(info_blocks: list[BeautifulSoup], city: str) -> None:
    if not info_blocks:
        logger.error(f'Error url: {city}.{Config.URL}')

    for block in info_blocks:
        name = block.find('div', attrs={'class': 'title'}).text.strip()
        date = block.find('time', attrs={'class': 'date date--md'}).text.strip()
        price = block.find('div', attrs={'class': 'cost rub'}).text.strip()
        link = block.find('a', attrs={'class': 'image js-ec-click-product'}).get('href')
        create_concert(name, reformat_date(date), reformat_price(price), city, link)


async def get_page_data(session: ClientSession, url: str) -> None:
    async with session.get(url, params=get_params()) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        city = get_city_from_url(url)
        fetch(soup.find_all('div', {'class': 'event-card js-ec-impression'}), city)
        logger.info(f'Parsed: {city}.{Config.URL}')


def check_out_dated() -> None:
    today = date.today()
    for concert in get_all_concerts():
        if concert.date < today:
            delete_concert_by_id(concert.id)


async def update_database() -> None:
    check_out_dated()
    urls = [f'https://{city}.{Config.URL}' for city in get_cities()]
    async with ClientSession(headers=get_header()) as session:
        await gather(*[get_page_data(session, url) for url in urls])
