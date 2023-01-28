from loguru import logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .parser import Parser
from bot.misc.utils import simplify_string


class KassirCitiesParser(Parser):
    _URLS = ('https://kassir.ru',)

    # region Private Methods

    @staticmethod
    def __get_city_from_url(url: str) -> str:
        url = urlparse(url).netloc
        return url[:url.find('.')]

    def __get_info_of_concert(self, info_block: BeautifulSoup) -> dict[str]:
        return {
            'abb': self.__get_city_from_url(info_block.get('href')),
            'name': info_block.text.strip(),
            'simple_name': simplify_string(info_block.text.strip())
        }

    def __get_info_from_info_blocks(self, info_blocks: list[BeautifulSoup]) -> list[dict[str]]:
        data_list = []
        for block in info_blocks:
            try:
                data_list.append(self.__get_info_of_concert(block))
            except Exception as e:
                logger.exception(e)
        return data_list

    # endregion

    # region Public Methods

    def fetch(self, page_data: str) -> list[dict[str]]:
        page_data = BeautifulSoup(page_data, 'lxml')
        city_block = page_data.find('div', attrs={
            'class': 'city-container-wrapper'
        })
        info_blocks = [block.find('a') for block in city_block.find_all('li')]
        return self.__get_info_from_info_blocks(info_blocks)

    # endregion
