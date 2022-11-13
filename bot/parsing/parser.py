from abc import ABC
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio import gather
from loguru import logger


# todo documentation and replace BeautifulSoup
class Parser(ABC):

    def __init__(self):
        self.urls = []
        self.params = {}
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    def fetch(self, page_data) -> list:
        pass

    async def get_page_data(self, session: ClientSession, url: str) -> list:
        async with session.get(url, params=self.params) as response:
            logger.info(f'Parsing: {response.url}')
            return self.fetch(BeautifulSoup(await response.text(), 'lxml'))

    async def get_data_from_all_urls(self) -> list:
        async with ClientSession(headers=self.header) as session:
            data = await gather(*[self.get_page_data(session, url) for url in self.urls])
        return sum(data, [])
