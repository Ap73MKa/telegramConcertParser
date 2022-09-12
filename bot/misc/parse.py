import httpx

from loguru import logger
from bs4 import BeautifulSoup
from bot.database.methods.create import create_concert
from bot.database.methods.get import get_all_concerts
from bot.misc.date import reformat_date


def get_concert_list() -> str:
    concert_list = reversed(get_all_concerts())
    return '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                      for concert in concert_list])


def update_database(link: str) -> None:
    __parse_info(__gather_info_blocks(link))


def __gather_info_blocks(link: str) -> list[BeautifulSoup]:
    soup = BeautifulSoup(httpx.get(link).text, 'lxml')
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
