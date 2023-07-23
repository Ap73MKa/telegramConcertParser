from re import sub
from urllib.parse import urlparse

import validators
from rapidfuzz.process import extractOne

from bot.database import get_all_cities, get_city_by_name_or_none
from bot.database.models import City


def simplify_string(name: str) -> str:
    return sub("[^a-zA-Zа-яА-Я]", "", name.lower().strip().replace("ё", "е"))


def get_netloc_from_url(url: str) -> str:
    if not url:
        raise ValueError("Empty URL provided")
    if not validators.url(url):
        raise ValueError("Invalid URL format")
    parsed_url = urlparse(url)
    netloc_parts = parsed_url.netloc.split(".")
    if len(netloc_parts) > 2:
        return netloc_parts[0]
    return ""


def fuzzy_recognize_city(title: str) -> City:
    if len(title) <= 2:
        raise ValueError("Title is too short")
    close = extractOne(
        simplify_string(title),
        [city.simple_name for city in get_all_cities()],
    )
    if close[1] < 80:
        raise ValueError("No matches")
    city = get_city_by_name_or_none(close[0])
    if not city:
        raise ValueError("No matches cities in database")
    return city
