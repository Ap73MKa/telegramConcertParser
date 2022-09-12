from os import environ
from typing import Final


class EnvKeys:
    TOKEN: Final = environ.get('TOKEN', 'define me')
    LINK: Final = environ.get('LINK', 'define me')
