import re
from collections.abc import Sequence
from datetime import date, datetime
from typing import ClassVar

from bs4 import BeautifulSoup, Tag
from loguru import logger

from src.config import configure

from .parser import GroupParser
from .utils import get_netloc_from_url


class KassirParser(GroupParser):
    _PARAMS: ClassVar[dict[str, str | int]] = {"sort": 1}

    def __init__(self, urls: Sequence[str]):
        self._URLS = urls
        self.ban_words = [
            "оркестр",
            "фестиваль",
            "джаз",
            "сертификат",
            "ансамбль",
            "абонемент",
            "симфон",
            "диско",
            "скрипка",
            "орган",
            "jazz",
            "xop",
            "театр",
            "премия",
            "радио",
            "radio",
            "фестиваля",
            "курс",
            "онлайн",
        ]

    # region Private Methods

    def __scrap_price(self, group: BeautifulSoup) -> int:
        price_element_wrapper = group.find(
            "li", {"class": "compilation-tile__price-block"}
        )
        if not isinstance(price_element_wrapper, Tag):
            return 0
        price_element = price_element_wrapper.find("span", {"class": "text-[0.65rem]"})
        if not isinstance(price_element, Tag):
            return 0
        return self.__reformat_price(price_element.text.strip())

    def __scrap_date(self, group: BeautifulSoup) -> date | None:
        date_element = group.find("time", {"class": "compilation-tile__date"})
        if not isinstance(date_element, Tag):
            return None
        datetime_string = date_element.get("datetime")
        if not datetime_string:
            return None
        return self.__reformat_date("".join(datetime_string))

    def __is_any_banned_word(self, string):
        return not any(word in string for word in self.ban_words)

    # region Static Methods

    @staticmethod
    def __reformat_date(concert_date: str) -> date | None:
        try:
            return datetime.strptime(concert_date, "%Y-%m-%dT%H:%M:%S%z").date()
        except ValueError:
            return None

    @staticmethod
    def __reformat_price(price: str) -> int:
        try:
            return int(re.sub(r"\D", "", price))
        except ValueError:
            return 0

    @staticmethod
    def __get_abb_from_url(page: BeautifulSoup) -> str:
        if not (meta_data := page.find("meta", {"property": "og:url"})):
            return ""
        url = meta_data.get("content") if isinstance(meta_data, Tag) else None
        if url is None:
            return ""
        try:
            return get_netloc_from_url("".join(url))
        except ValueError:
            return ""

    @staticmethod
    def __prepare_data(scraped_data: Sequence[dict], city_abb: str):
        scraped_data = [
            {**item, "link": f"https://{city_abb}.kassir.ru" + item["link"]}
            for item in scraped_data
        ]
        return [dict(item, **{"city_abb": city_abb}) for item in scraped_data]

    @staticmethod
    def __scrap_name(group: BeautifulSoup) -> str:
        name_element = group.find("div", {"class": "compilation-tile__title"})
        return name_element.text.strip() if name_element else ""

    @staticmethod
    def __scrap_link(group: BeautifulSoup) -> str:
        link_element = group.find("a", {"class": "compilation-tile__img-block"})
        link = link_element.get("href") if isinstance(link_element, Tag) else ""
        return "".join(link) if link else ""

    # endregion

    def _is_valid_data(self, data: dict) -> bool:
        if not all(data[key] for key in data.keys()):
            return False
        if data["price"] < 500:
            return False
        return self.__is_any_banned_word(data["name"])

    def _scrap_data_group(self, group: BeautifulSoup) -> dict:
        return {
            "name": self.__scrap_name(group),
            "date": self.__scrap_date(group),
            "price": self.__scrap_price(group),
            "link": self.__scrap_link(group),
        }

    def _parse_page_data(self, page_data: str) -> Sequence[dict]:
        soup_data = BeautifulSoup(page_data, "lxml")
        info_blocks = soup_data.find_all(
            "article", {"class": "recommendation-item compilation-tile"}
        )
        if not (city_abb := self.__get_abb_from_url(soup_data)) or not info_blocks:
            logger.warning(
                f"No info from https://{city_abb if city_abb else 'UNDEFINED'}.{configure.bot.kassir_link}"
            )
            return []
        return self.__prepare_data(self._scrap_all_data(info_blocks), city_abb)

    # endregion
