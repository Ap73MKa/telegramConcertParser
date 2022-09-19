import httpx

from loguru import logger
from bs4 import BeautifulSoup
from bot.database.methods.create import create_concert
from bot.database.methods.get import get_all_concerts
from user_agent import generate_user_agent
from .date import reformat_date


def get_concert_list() -> str:
    concert_list = reversed(get_all_concerts())
    return '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                      for concert in concert_list])


def update_database() -> None:
    url = 'https://afisha.yandex.ru/vladimir/selections/all-events-concert'
    __parse_info(__gather_info_blocks(__get_http(url)))


def __get_http(url: str) -> str:
    header = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux')),
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    try:
        page_response = httpx.get(url, timeout=15, headers=header, follow_redirects=True)
        logger.info(f'Status code: {page_response.status_code}')
        return page_response.text
    except httpx.Timeout as e:
        logger.info("It is time to timeout")
        logger.error(str(e))
        return ''


def __gather_info_blocks(site: str) -> list[BeautifulSoup]:
    soup = BeautifulSoup(site, 'lxml')
    return soup.find_all('div', {'class': 'Inner-sc-5s87mw-1 fXrHG'})


def __parse_info(info_blocks: list[BeautifulSoup]) -> None:
    if not info_blocks:
        logger.error('Parsing error')
        return

    for block in info_blocks:
        name = block.find('h2', attrs={'class': 'Title-sc-5meihc-3 eOlfER'}).text
        date = block.find('li', attrs={'class': 'DetailsItem-sc-5meihc-1 gzFGVO'}).text
        price = block.find('span', attrs={'class': 'PriceBlock-bp958r-11 cNqIOh'}).text
        price = int(''.join(filter(str.isdigit, price)))
        pos = date.find(',')
        create_concert(name, reformat_date(date[:pos]), price)

    logger.info('Page successfully parsed')
