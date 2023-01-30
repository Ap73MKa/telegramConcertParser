from abc import ABC, abstractmethod
from asyncio import gather
from aiohttp import ClientSession

from bs4 import BeautifulSoup
from loguru import logger


class Parser(ABC):
    # TODO: new dataclass or NamedTuple
    _URLS = ()
    _PARAMS = {}
    _HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    # region Private Methods
    @abstractmethod
    def _fetch(self, page_data: str) -> list:
        pass

    async def __get_page_data(self, session: ClientSession, url: str) -> list:
        async with session.get(url, params=self._PARAMS) as response:
            return self._fetch(await response.text())

    # endregion

    # region Public Methods
    async def get_data_from_all_urls(self) -> list:
        async with ClientSession(headers=self._HEADER) as session:
            return sum(await gather(*[self.__get_page_data(session, url) for url in self._URLS]), [])

    # endregion


class GroupParser(Parser, ABC):

    # region Private Methods
    def __filter_data(self, data: BeautifulSoup) -> dict | None:
        try:
            data = self._scrap_data_group(data)
            if self._is_good_data(data):
                return data
        except Exception as e:
            logger.exception(e)
        return None

    @abstractmethod
    def _scrap_data_group(self, group: BeautifulSoup) -> dict:
        pass

    @abstractmethod
    def _is_good_data(self, data: dict) -> bool:
        return True

    def _scrap_all_data(self, data_groups: list[BeautifulSoup]) -> list[dict[str]]:
        return [item for item in [self.__filter_data(group) for group in data_groups] if item is not None]

    # endregion
