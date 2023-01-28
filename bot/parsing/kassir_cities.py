from bs4 import BeautifulSoup

from .parser import GroupParser
from bot.misc.utils import simplify_string


class KassirCitiesParser(GroupParser):
    _URLS = ('https://kassir.ru',)

    def scrap_data_group(self, group: BeautifulSoup) -> dict:
        return {'abb': get_city_from_url(group.get('href')),
                'name': group.text.strip(),
                'simple_name': simplify_string(group.text.strip())}

    def fetch(self, page_data: str) -> list[dict[str]]:
        data_groups = BeautifulSoup(page_data, 'lxml').find('div', attrs={'class': 'city-container-wrapper'})
        return self.scrap_all_data([group.find('a') for group in data_groups.find_all('li')])
