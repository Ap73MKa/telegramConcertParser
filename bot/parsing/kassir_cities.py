from bs4 import BeautifulSoup

from bot.modules.simplify import simplify_string, get_city_from_url
from .parser import GroupParser


class KassirCities(GroupParser):

    def __init__(self):
        super().__init__()
        self.urls = ['https://kassir.ru']

    def scrap_data_group(self, group: BeautifulSoup) -> dict:
        return {'abb': get_city_from_url(group.get('href')),
                'name': group.text.strip(),
                'simple_name': simplify_string(group.text.strip())}

    def fetch(self, page_data: str) -> list[dict[str]]:
        data_groups = BeautifulSoup(page_data, 'lxml').find('div', attrs={'class': 'city-container-wrapper'})
        return self.scrap_all_data([group.find('a') for group in data_groups.find_all('li')])
