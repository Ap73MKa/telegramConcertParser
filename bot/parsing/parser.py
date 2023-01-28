from abc import ABC
from asyncio import gather
from aiohttp import ClientSession


class Parser(ABC):
    # TODO: new dataclass or NamedTuple
    _URLS = ()
    _PARAMS = {}
    _HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    # region Private Methods

    async def __get_page_data(self, session: ClientSession, url: str) -> list:
        async with session.get(url, params=self._PARAMS) as response:
            return self.fetch(await response.text())

    # endregion

    # region Public Methods

    def fetch(self, page_data: str) -> list:
        raise NotImplementedError

    async def get_data_from_all_urls(self) -> list:
        async with ClientSession(headers=self._HEADER) as session:
            data = await gather(*[self.__get_page_data(session, url) for url in self._URLS])
            return sum(data, [])

    # endregion
