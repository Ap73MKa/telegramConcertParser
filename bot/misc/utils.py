from re import sub
from urllib.parse import urlparse


def simplify_string(name: str) -> str:
    return sub("[^a-zA-Zа-яА-Я]", "", name.lower().strip().replace("ё", "е"))


def get_city_from_url(url: str) -> str:
    url = urlparse(url).netloc
    return url[: url.find(".")]
