from locale import setlocale, LC_ALL
from datetime import date, datetime
from urllib.parse import urlparse
from loguru import logger


def set_language() -> None:
    setlocale(LC_ALL, ('ru_RU', 'UTF-8'))
    logger.info('Language changed to Russian')


def reformat_date(concert_date: str) -> date:
    concert_date = datetime.strptime(concert_date[:6].lower(), '%d %b').date()
    year = date.today().year + 1 if concert_date.month < date.today().month else date.today().year
    return concert_date.replace(year=year)


def reformat_price(price: str) -> int:
    pos = price.find('—')
    price = price[:pos] if pos != 0 else price
    return int(''.join(filter(str.isdigit, price)))


def get_city_from_url(url: str) -> str:
    url = urlparse(url).netloc
    return url[:url.find('.')]


def get_cities():
    return {
        'msk': 'Москва',
        'spb': 'Санкт-Петербург',
        'nn': 'Нижний Новгород',
        'rnd': 'Ростов-на-Дону',
        'kzn': 'Казань',
        'vlm': 'Владимир'
    }
