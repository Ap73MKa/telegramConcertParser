from bs4 import BeautifulSoup

from bot.misc import simplify_string, get_city_from_url
from .parser import GroupParser


class KassirCitiesParser(GroupParser):
    _URLS = ("https://kassir.ru",)

    def _is_valid_data(self, data: dict) -> bool:
        return True

    def _scrap_data_group(self, group: BeautifulSoup) -> dict:
        return {
            "abb": get_city_from_url(group.get("href")),
            "name": group.text.strip(),
            "simple_name": simplify_string(group.text.strip()),
        }

    def _parse_page_data(self, page_data: str) -> list[dict[str]]:
        data_groups = BeautifulSoup(page_data, "lxml").find(
            "div", attrs={"class": "city-container-wrapper"}
        )
        return self._scrap_all_data(
            [group.find("a") for group in data_groups.find_all("li")]
        )
