from os import environ
from typing import Final


class Config:
    TOKEN: Final = environ.get('TOKEN', 'define me')
    KASSIR_SITE = 'kassir.ru/bilety-na-koncert?'
    DATABASE = 'database.db'
