from typing import NamedTuple
from loguru import logger
from bs4 import BeautifulSoup
from httpx import Client, HTTPError
from proxyscrape import create_collector
from ..database.methods.create import create_concert
from .reformat import reformat_date, reformat_price
from .singleton import SingletonMeta
from .config import Config


class CategoryId(NamedTuple):
    HUMOR = 4073
    HIP_HOP = 3007
    ELECTRONIC = 3008
    ROCK = 3002
    POP = 3003


class Requester(metaclass=SingletonMeta):
    def __init__(self):
        self.proxies = create_collector('my-collector', 'http')

    def generate_proxy(self) -> str:
        proxy = self.proxies.get_proxy()
        logger.info(f'IP: {proxy.host}:{proxy.port}')
        return f'{proxy.host}:{proxy.port}'

    def get_http(self, url: str, params=None) -> str:
        if params is None:
            params = {}
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            proxy = {'http://': f'http://{self.generate_proxy()}'}
            with Client(headers=header, proxies=proxy, follow_redirects=True) as client:
                page_response = client.get(url, timeout=5, params=params)
            logger.info(f'Page status: {page_response.status_code}')
            return page_response.text

        except HTTPError as exc:
            logger.error(str(exc))
            return ''


class Kassir:
    def __init__(self):
        self.url: str = Config.URL
        self.params: dict = {
            'category[]': [CategoryId.HUMOR, CategoryId.ELECTRONIC, CategoryId.HIP_HOP,
                           CategoryId.ROCK, CategoryId.POP],
            'sort': 0,
            'c': 30
        }

    @staticmethod
    def parse(site: str) -> None:
        soup = BeautifulSoup(site, 'lxml')
        info_blocks = soup.find_all('div', {'class': 'event-card__caption'})

        if not info_blocks:
            logger.error('Incorrect input info')
            return

        for block in info_blocks:
            name = block.find('div', attrs={'class': 'title'}).text.strip()
            date = block.find('time', attrs={'class': 'date date--md'}).text.strip()
            price = block.find('div', attrs={'class': 'cost rub'}).text.strip()
            create_concert(name, reformat_date(date), reformat_price(price))


def update_database() -> None:
    Kassir().parse(Requester().get_http(Kassir().url, Kassir().params))
