from typing import NamedTuple
from datetime import date, datetime
from bs4 import BeautifulSoup
from loguru import logger
from urllib.parse import urlparse

from .parser import Parser
from .utils import get_cities
from bot.misc import Config


class CategoryId(NamedTuple):
    HUMOR = 4073
    HIP_HOP = 3007
    ELECTRONIC = 3008
    ROCK = 3002
    POP = 3003


class Kassir(Parser):

    urls = [f'https://{city}.{Config.KASSIR_SITE}' for city in get_cities()]
    params = {
        'category[]': [CategoryId.HUMOR,
                       CategoryId.ELECTRONIC,
                       CategoryId.HIP_HOP,
                       CategoryId.ROCK,
                       CategoryId.POP],
        'sort': 0,
        'c': 30
    }

    @staticmethod
    def __reformat_date(concert_date: str) -> date:
        concert_date = datetime.strptime(concert_date[:6].lower(), '%d %b').date()
        year = date.today().year + 1 if concert_date.month < date.today().month else date.today().year
        return concert_date.replace(year=year)

    @staticmethod
    def __reformat_price(price: str) -> int:
        pos = price.find('—')
        price = price[:pos] if pos != 0 else price
        return int(''.join(filter(str.isdigit, price)))

    @staticmethod
    def __get_city_from_url(url: str) -> str:
        url = urlparse(url).netloc
        return url[:url.find('.')]

    def __create_concert_on_data(self, info_block: BeautifulSoup, city: str) -> dict[str]:
        return {
            'name': info_block.find('div', attrs={'class': 'title'}).text.strip(),
            'date': self.__reformat_date(info_block.find('time', attrs={'class': 'date date--md'}).text.strip()),
            'price': self.__reformat_price(info_block.find('div', attrs={'class': 'cost rub'}).text.strip()),
            'link': info_block.find('a', attrs={'class': 'image js-ec-click-product'}).get('href'),
            'city': city
        }

    def fetch(self, page_data: BeautifulSoup, url: str) -> tuple[dict[str]]:
        info_blocks = page_data.find_all('div', {'class': 'event-card js-ec-impression'})
        city = self.__get_city_from_url(url)
        if not info_blocks:
            logger.error(f'Error url: {url}')
        my_list = []
        for info_block in info_blocks:
            try:
                my_list.append(self.__create_concert_on_data(info_block, city))
            except:
                print('got error')
        return tuple(my_list)
