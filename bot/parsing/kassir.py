import re
from datetime import date, datetime
from bs4 import BeautifulSoup
from loguru import logger

from bot.modules import Config
from bot.database import get_all_cities
from bot.modules.simplify import get_city_from_url
from .parser import GroupParser


class Kassir(GroupParser):
    def __init__(self):
        super().__init__()
        self.urls = [
            f"https://{city.abb}.{Config.KASSIR_SITE}" for city in get_all_cities()
        ]
        self.params = {"sort": 0, "c": 60}
        self.ban_words = Config.BAN_WORDS

    @staticmethod
    def __reformat_date(concert_date: str) -> date:
        return datetime.strptime(concert_date, "%Y-%m-%dT%H:%M:%S%z").date()

    @staticmethod
    def __reformat_price(price: str) -> int:
        return int(re.sub(r"\D", "", price))

    def is_good_data(self, data: dict) -> bool:
        if not all(data[key] for key in data.keys()):
            return False
        if data["price"] < 500:
            return False
        for word in self.ban_words:
            if word in data["name"]:
                return False
        return True

    def scrap_data_group(self, data_groups: BeautifulSoup) -> dict[str]:
        return {
            "name": data_groups.find(
                "div", {"class": "compilation-tile__title"}
            ).text.strip(),
            "date": self.__reformat_date(
                data_groups.find("time", {"class": "compilation-tile__date"}).get(
                    "datetime"
                )
            ),
            "price": self.__reformat_price(
                data_groups.find("li", {"class": "compilation-tile__price-block"})
                .find("span", {"class": "text-[0.65rem]"})
                .text.strip()
            ),
            "link": data_groups.find("a", {"class": "compilation-tile__img-block"}).get(
                "href"
            ),
        }

    def fetch(self, page_data: str) -> list[dict[str]]:
        page_data = BeautifulSoup(page_data, "lxml")
        url = page_data.find("meta", {"property": "og:url"}).get("content")
        city_abb = get_city_from_url(url)
        info_blocks = page_data.find_all(
            "article", {"class": "recommendation-item compilation-tile"}
        )
        if not info_blocks:
            logger.warning(f"No info from {url}")
        scraped_data = self.scrap_all_data(info_blocks)
        scraped_data = [
            {**item, "link": f"https://{city_abb}.kassir.ru" + item["link"]}
            for item in scraped_data
        ]
        return [dict(item, **{"city": city_abb}) for item in scraped_data]
