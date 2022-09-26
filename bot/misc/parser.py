import asyncio
from typing import NamedTuple
from loguru import logger
from bs4 import BeautifulSoup
from httpx import HTTPError, AsyncClient
from proxyscrape import create_collector
from ..database.methods.create import create_concert
from .reformat import reformat_date, reformat_price, get_cities
from .config import Config


class CategoryId(NamedTuple):
    HUMOR = 4073
    HIP_HOP = 3007
    ELECTRONIC = 3008
    ROCK = 3002
    POP = 3003


class Proxy:
    proxies = create_collector('my-collector', 'http')

    def generate_proxy(self) -> str:
        proxy = self.proxies.get_proxy()
        logger.info(f'IP: {proxy.host}:{proxy.port}')
        return f'{proxy.host}:{proxy.port}'


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
    async def parse(site: str, city: str) -> None:
        soup = BeautifulSoup(site, 'lxml')
        info_blocks = soup.find_all('div', {'class': 'event-card__caption'})

        if not info_blocks:
            logger.error('Incorrect input info')
            return

        for block in info_blocks:
            name = block.find('div', attrs={'class': 'title'}).text.strip()
            date = block.find('time', attrs={'class': 'date date--md'}).text.strip()
            price = block.find('div', attrs={'class': 'cost rub'}).text.strip()
            create_concert(name, reformat_date(date), reformat_price(price), city)


async def get_http(url: str, proxy=None, params=None) -> str:
    params = {} if params is None else params
    proxy = {} if proxy is None else {'http://': f'http://{proxy}'}
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        async with AsyncClient(headers=header, proxies=proxy, follow_redirects=True) as client:
            page_response = await client.get(url, timeout=5, params=params)
        logger.info(f'Page status: {page_response.status_code} URL: {page_response.url}')
        return page_response.text

    except HTTPError as exc:
        logger.error(str(exc))
        return ''


async def update_database() -> None:
    logger.info('Start parsing')
    task = []
    proxy = Proxy().generate_proxy()
    for city in get_cities().keys():
        url = f'https://{city}.{Kassir().url}'
        page = await get_http(url, proxy, Kassir().params)
        task.append(Kassir().parse(page, city))
    await asyncio.gather(*task)
    logger.info('Parse completed')
