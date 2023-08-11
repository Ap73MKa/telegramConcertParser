from collections.abc import Sequence
from typing import ClassVar

from bs4 import BeautifulSoup, Tag

from src.config import configure

from .parser import GroupParser
from .utils import get_netloc_from_url, simplify_string


class KassirCitiesParser(GroupParser):
    _URLS: ClassVar[list[str]] = [f"https://{configure.bot.kassir_link}"]

    def _is_valid_data(self, data: dict) -> bool:
        if not all(data[key] for key in data.keys()):
            return False
        return True

    def _scrap_data_group(self, group: BeautifulSoup) -> dict:
        main_element = group.find("a")
        if not isinstance(main_element, Tag):
            return {}
        url = main_element.get("href")
        text = main_element.text.strip()
        return {
            "abb": get_netloc_from_url("".join(url) if url else ""),
            "name": text,
            "simplified_name": simplify_string(text),
        }

    def _parse_page_data(self, page_data: str) -> Sequence[dict[str, str]]:
        soup_data = BeautifulSoup(page_data, "lxml")
        city_list_wrapper = soup_data.find("div", {"class": "city-container-wrapper"})
        if not isinstance(city_list_wrapper, Tag):
            return []
        city_list_elements = city_list_wrapper.find_all("li")
        return self._scrap_all_data(city_list_elements)
