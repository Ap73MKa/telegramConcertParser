import httpx

from typing import NamedTuple
from loguru import logger
from bs4 import BeautifulSoup
from proxyscrape import create_collector, get_collector
from bot.database.methods.create import create_concert
from bot.database.methods.get import get_all_concerts
from .date import reformat_date


class CategoryId(NamedTuple):
    HUMOR = 4073
    HIP_HOP = 3007
    ELECTRO = 3008
    ROCK = 3002
    POP = 3003


def register_network() -> None:
    create_collector('my-collector', 'http')


def get_concert_list() -> str:
    concert_list = reversed(get_all_concerts())
    return '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                      for concert in concert_list])


def update_database() -> None:
    url = 'https://vlm.kassir.ru/bilety-na-koncert?'

    params = {
        'category[]': [
            CategoryId.HUMOR,
            CategoryId.ELECTRO,
            CategoryId.HIP_HOP,
            CategoryId.ROCK,
            CategoryId.POP
        ],
        'sort': 1
    }

    __parse_kassir(__get_http(url, params))


def __generate_proxy() -> str:
    proxy = get_collector('my-collector').get_proxy()
    ip = f'{proxy.host}:{proxy.port}'
    logger.info(f'IP: {ip}')
    return ip


def __get_http(url: str, params=None) -> str:

    if params is None:
        params = {}

    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:104.0) Gecko/20100101 Firefox/104.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

        proxy = {'http://': f'http://{__generate_proxy()}'}

        with httpx.Client(headers=header, proxies=proxy, follow_redirects=True) as client:
            page_response = client.get(url, timeout=5, params=params)
        logger.info(f'Page status: {page_response.status_code}')
        return page_response.text

    except Exception as e:
        logger.error(str(e))
        return ''


def __parse_kassir(site: str) -> None:
    soup = BeautifulSoup(site, 'lxml')
    info_blocks = soup.find_all('div', {'class': 'event-card__caption'})

    if not info_blocks:
        logger.error('Incorrect input info')
        return

    for block in info_blocks:
        name = block.find('div', attrs={'class': 'title'}).text.strip()

        date = block.find('time', attrs={'class': 'date date--md'}).text.strip()
        pos = date.find('.')
        print(date[:pos])
        date = reformat_date(date[:pos])

        price = block.find('div', attrs={'class': 'cost rub'}).text.strip()
        pos = price.find('—')
        price = price[:pos] if pos != 0 else price
        price = int(''.join(filter(str.isdigit, price)))

        create_concert(name, date, price)
