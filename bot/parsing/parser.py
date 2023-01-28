from abc import ABC, abstractmethod
from asyncio import gather
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger


class Parser(ABC):

    def __init__(self):
        self.urls = []
        self.params = {}
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    @abstractmethod
    def fetch(self, page_data: str) -> list:
        pass

    async def get_page_data(self, session: ClientSession, url: str) -> list:
        async with session.get(url, params=self.params) as response:
            return self.fetch(await response.text())

    async def get_data_from_all_urls(self) -> list:
        async with ClientSession(headers=self.header) as session:
            return sum(await gather(*[self.get_page_data(session, url) for url in self.urls]), [])


class GroupParser(Parser, ABC):

    @abstractmethod
    def scrap_data_group(self, group: BeautifulSoup) -> dict:
        pass

    @staticmethod
    def is_good_data(data: dict) -> bool:
        return True

    def scrap_all_data(self, data_groups: list[BeautifulSoup]) -> list[dict[str]]:
        return [item for item in [self.__filter_data(group) for group in data_groups] if item is not None]

    def __filter_data(self, data: BeautifulSoup) -> dict | None:
        try:
            data = self.scrap_data_group(data)
            if self.is_good_data(data):
                return data
        except Exception as e:
            logger.exception(e)
        return None
