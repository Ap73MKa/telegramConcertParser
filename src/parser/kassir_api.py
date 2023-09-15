from asyncio import gather
from collections.abc import Sequence
from datetime import date, datetime
from typing import ClassVar, NamedTuple, TypedDict

from aiohttp import ClientSession
from config import configure
from loguru import logger


class PriceRange(TypedDict):
    min: int
    max: int


class ResponseItem(TypedDict):
    id: int
    title: str
    beginsAt: str
    priceRange: PriceRange
    urlSlug: str
    isMultiDay: bool


class ResponseObject(TypedDict):
    object: ResponseItem


class Response(TypedDict):
    items: Sequence[ResponseObject]


class ResultItem(NamedTuple):
    name: str
    date: date
    price: int
    link: str
    city_abb: str


class KassirApi:
    _HEADER: ClassVar[dict[str, str]] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    _PARAMS: ClassVar[dict[str, str | int]] = {
        "currentPage": 1,
        "pageSize": 100,
        "sortMode": 0,
        "categoryId": 3000,
        "domain": "",
    }

    def __init__(self, domains: Sequence[str]):
        self.domains = domains

    async def get_data_from_api(self) -> Sequence[ResultItem]:
        async with ClientSession(headers=self._HEADER) as session:
            result = await gather(
                *[self.fetch(session, domain) for domain in self.domains]
            )
            return [item for sublist in result for item in sublist if item]

    async def fetch(
        self, session: ClientSession, domain: str
    ) -> Sequence[ResultItem | None]:
        params = {**self._PARAMS, "domain": domain}
        abb = domain.split(".")[0]
        try:
            async with session.get(configure.bot.kassir_api, params=params) as response:
                json_response: Response = await response.json(encoding="UTF-8")
                return [
                    self.parse_data(item["object"], abb)
                    for item in json_response["items"]
                ]
        except Exception as e:
            logger.exception(
                f"An error occurred while fetching data from {abb}.{configure.bot.kassir_site}: {e}"
            )
            return []

    @staticmethod
    def parse_data(item: ResponseItem, abb: str) -> ResultItem | None:
        try:
            keys = ["beginsAt", "title", "priceRange", "urlSlug"]
            if not all(key in item for key in keys):
                return None
            return ResultItem(
                name=item["title"].strip(),
                date=datetime.strptime(item["beginsAt"], "%Y-%m-%dT%H:%M:%S%z").date(),
                price=int(item["priceRange"]["min"]),
                link=f'https://{abb}.{configure.bot.kassir_site}/{item["urlSlug"]}',
                city_abb=abb,
            )
        except Exception as e:
            logger.exception(e)
            return None
