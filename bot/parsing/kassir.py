import re
from datetime import date, datetime

from loguru import logger
from bs4 import BeautifulSoup

from bot.misc import Config, get_city_from_url
from bot.database import get_all_cities_or_none
from .parser import GroupParser


class KassirParser(GroupParser):
    _PARAMS = {"sort": 0, "c": 60}

    def __init__(self):
        self._URLS = (
            f"https://{city.abb}.{Config.KASSIR_SITE}"
            for city in get_all_cities_or_none()
        )
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
            "хор",
            "театр",
            "премия",
            "радио",
            "radio",
            "фестиваля",
        ]

    # region Private Methods

    # region Static Methods

    @staticmethod
    def __reformat_date(concert_date: str) -> date:
        return datetime.strptime(concert_date, "%Y-%m-%dT%H:%M:%S%z").date()

    @staticmethod
    def __reformat_price(price: str) -> int:
        return int(re.sub(r"\D", "", price))

    # endregion

    def _is_good_data(self, data: dict) -> bool:
        if not all(data[key] for key in data.keys()):
            return False
        if data["price"] < 500:
            return False
        for word in self.ban_words:
            if word in data["name"]:
                return False
        return True

    def _scrap_data_group(self, group: BeautifulSoup) -> dict[str]:
        return {
            "name": group.find(
                "div", {"class": "compilation-tile__title"}
            ).text.strip(),
            "date": self.__reformat_date(
                group.find("time", {"class": "compilation-tile__date"}).get("datetime")
            ),
            "price": self.__reformat_price(
                group.find("li", {"class": "compilation-tile__price-block"})
                .find("span", {"class": "text-[0.65rem]"})
                .text.strip()
            ),
            "link": group.find("a", {"class": "compilation-tile__img-block"}).get(
                "href"
            ),
        }

    def _fetch(self, page_data: str) -> list[dict[str]]:
        page_data = BeautifulSoup(page_data, "lxml")
        meta_data = page_data.find("meta", {"property": "og:url"})
        if not meta_data:
            return []
        url = meta_data.get("content")
        city_abb = get_city_from_url(url)
        info_blocks = page_data.find_all(
            "article", {"class": "recommendation-item compilation-tile"}
        )
        if not info_blocks:
            logger.warning(f"No info from {url}")
            return []
        scraped_data = self._scrap_all_data(info_blocks)
        scraped_data = [
            {**item, "link": f"https://{city_abb}.kassir.ru" + item["link"]}
            for item in scraped_data
        ]
        return [dict(item, **{"city": city_abb}) for item in scraped_data]

    # endregion
