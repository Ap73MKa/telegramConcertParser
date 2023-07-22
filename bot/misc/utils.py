from re import sub
import validators
from urllib.parse import urlparse


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
