from datetime import date, datetime

from loguru import logger
from bs4 import BeautifulSoup

from bot.misc import Config, get_city_from_url
from bot.database import get_all_cities_or_none
from .parser import GroupParser


class KassirParser(GroupParser):
    _PARAMS = {'sort': 0, 'c': 60}

    def __init__(self):
        self._URLS = (
            f'https://{city.abb}.{Config.KASSIR_SITE}' for city in get_all_cities_or_none()
        )
        self.ban_words = [
            'оркестр', 'фестиваль', 'джаз', 'сертификат', 'ансамбль', 'абонемент', 'симфон', 'диско',
            'скрипка', 'орган', 'jazz', 'хор', 'театр', 'премия', 'радио', 'radio', 'фестиваля'
        ]

    # region Private Methods

    # region Static Methods

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

    # endregion

    def _is_good_data(self, data: dict) -> bool:
        if data['price'] < 500:
            return False
        for word in self.ban_words:
            if word in data['name']:
                return False
        return True

    def _scrap_data_group(self, info_block: BeautifulSoup) -> dict[str]:
        return {
            'name': info_block.find('div', attrs={'class': 'title'}).text.strip(),
            'date': self.__reformat_date(info_block.find('time', attrs={'class': 'date date--md'}).text.strip()),
            'price': self.__reformat_price(info_block.find('div', attrs={'class': 'cost rub'}).text.strip()),
            'link': info_block.find('a', attrs={'class': 'image js-ec-click-product'}).get('href')
        }

    def _fetch(self, page_data: str) -> list[dict[str]]:
        page_data = BeautifulSoup(page_data, 'lxml')
        city_abb = get_city_from_url(page_data.find('link', {'rel': 'canonical'}).get('href'))
        info_blocks = page_data.find_all('div', {'class': 'event-card js-ec-impression js-ec-tile'})
        if not info_blocks:
            logger.warning(f'No info from https://{city_abb}.{Config.KASSIR_SITE}')
        return [dict(item, **{'city': city_abb}) for item in self._scrap_all_data(info_blocks)]

    # endregion
