from os import environ
from typing import Final


class Config:
    TOKEN: Final = environ.get("TOKEN", "define me")
    DEBUG: Final = bool(len(environ.get("DEBUG", "")))
    ADMIN_ID: Final = environ.get("ADMIN_ID", "define me")
    KASSIR_SITE: Final = "kassir.ru/bilety-na-koncert?"
