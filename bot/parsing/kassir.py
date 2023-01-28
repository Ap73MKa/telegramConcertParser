from datetime import date, datetime

from loguru import logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from bot.misc import Config
from bot.database import get_all_cities_or_none
from .parser import Parser


class KassirParser(Parser):

    _PARAMS = {'sort': 0, 'c': 60}

    # region Private Methods

    def __init__(self):
        self._URLS = (
            f'https://{city.abb}.{Config.KASSIR_SITE}' for city in get_all_cities_or_none()
        )

    # region Static Methods
    @staticmethod
    def __is_good_name(name: str) -> bool:
        ban_words = (
            'оркестр', 'фестиваль', 'джаз', 'сертификат', 'ансамбль', 'абонемент', 'симфон', 'диско',
            'скрипка', 'орган', 'jazz', 'хор', 'театр', 'премия', 'радио', 'radio', 'фестиваля'
        )
        for word in ban_words:
            if word in name:
                return False
        return True

    @staticmethod
    def __reformat_date(concert_date: str) -> date:
        if not any(map(str.isdigit, concert_date)):
            return date.today()
        day, month = concert_date.split()[:2]
        month = month[:3].lower()
        if month == 'май':
            concert_date = date(2022, 5, int(day))
        else:
            concert_date = datetime.strptime(' '.join([day, month]), '%d %b').date()
        year = date.today().year + 1 if concert_date.month < date.today().month else date.today().year
        return concert_date.replace(year=year)

    @staticmethod
    def __reformat_price(price: str) -> int:
        if not any(map(str.isdigit, price)):
            return 0
        pos = price.find('—')
        price = price[:pos] if pos != -1 else price
        return int(''.join(filter(str.isdigit, price)))

    @staticmethod
    def __get_city_from_url(url: str) -> str:
        url = urlparse(url).netloc
        return url[:url.find('.')]

    # endregion

    def __get_data_of_concert(self, info_block: BeautifulSoup) -> dict[str]:
        return {
            'name': info_block.find('div', attrs={'class': 'title'}).text.strip(),
            'date': self.__reformat_date(info_block.find('time', attrs={'class': 'date date--md'}).text.strip()),
            'price': self.__reformat_price(info_block.find('div', attrs={'class': 'cost rub'}).text.strip()),
            'link': info_block.find('a', attrs={'class': 'image js-ec-click-product'}).get('href')
        }

    def __get_data_from_info_blocks(self, info_blocks: list[BeautifulSoup]) -> list[dict[str]]:
        data_list = []
        for block in info_blocks:
            try:
                data = self.__get_data_of_concert(block)
                if not self.__is_good_name(data['name'].lower()) or data['price'] < 500:
                    continue
                data_list.append(data)
            except Exception as e:
                logger.exception(e)
        return data_list

    # endregion

    # region Public Methods

    def fetch(self, page_data: str) -> list[dict[str]]:
        page_data = BeautifulSoup(page_data, 'lxml')
        city_abb = self.__get_city_from_url(page_data.find('link', {'rel': 'canonical'}).get('href'))
        info_blocks = page_data.find_all('div', {'class': 'event-card js-ec-impression js-ec-tile'})
        return [dict(item, **{'city': city_abb}) for item in self.__get_data_from_info_blocks(info_blocks)]

    # endregion

