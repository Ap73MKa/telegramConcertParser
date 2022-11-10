from abc import ABC
from bs4 import BeautifulSoup
from loguru import logger
from aiohttp import ClientSession
from asyncio import gather


class Parser(ABC):

    urls = []
    params = {}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    def fetch(self, page_data: BeautifulSoup, url: str) -> None:
        pass

    async def get_page_data(self, session, url) -> None:
        async with session.get(url, params=self.params) as response:
            self.fetch(BeautifulSoup(await response.text(), 'lxml'), url)
            logger.info(f'Parsing completed: {url}')

    async def get_data_from_all_urls(self) -> None:
        async with ClientSession(headers=self.header) as session:
            await gather(*[self.get_page_data(session, url) for url in self.urls])