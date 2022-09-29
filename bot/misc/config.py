from os import environ
from typing import Final


class Config:
    TOKEN: Final = environ.get('TOKEN', 'define me')
    LINK: Final = environ.get('LINK', 'define me')
    URL: Final = 'kassir.ru/bilety-na-koncert?'
