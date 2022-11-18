from typing import NamedTuple
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from loguru import logger

from .parser import Parser
from bot.modules.simplify import simplify_string


class CategoryId(NamedTuple):
    HUMOR = 4073
    HIP_HOP = 3007
    ELECTRONIC = 3008
    ROCK = 3002
    POP = 3003


class KassirCities(Parser):

    def __init__(self):
        super().__init__()
        self.urls = ['https://kassir.ru']

    @staticmethod
    def __get_city_from_url(url: str) -> str:
        url = urlparse(url).netloc
        return url[:url.find('.')]

    def __get_data_of_concert(self, info_block: BeautifulSoup) -> dict[str]:
        return {'abb': self.__get_city_from_url(info_block.get('href')),
                'name': info_block.text.strip(),
                'simple_name': simplify_string(info_block.text.strip())}

    def __get_data_from_info_blocks(self, info_blocks: list[BeautifulSoup]) -> list[dict[str]]:
        data_list = []
        for block in info_blocks:
            try:
                data_list.append(self.__get_data_of_concert(block))
            except Exception as e:
                logger.exception(e)
        return data_list

    def fetch(self, page_data: str) -> list[dict[str]]:
        page_data = BeautifulSoup(page_data, 'lxml')
        city_block = page_data.find('div', attrs={'class': 'city-container-wrapper'})
        info_blocks = city_block.find_all('li')
        info_blocks = [block.find('a') for block in info_blocks]
        return self.__get_data_from_info_blocks(info_blocks)
