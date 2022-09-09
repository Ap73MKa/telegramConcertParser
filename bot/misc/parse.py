import httpx

from loguru import logger
from bs4 import BeautifulSoup
from bot.database.methods.create import create_concert
from bot.database.methods.get import get_all_concerts
from bot.misc.date import reformat_date


def get_concert_list() -> str:
    concert_list = get_all_concerts()
    concert_list.reverse()
    return '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                      for concert in concert_list])


def parse_page(link: str):
    page = httpx.get(link).text
    soup = BeautifulSoup(page, 'lxml')
    concerts = soup.find_all('div', {'class': 'Inner-sc-5s87mw-1 fXrHG'})

    if not concerts:
        logger.error('Parsing error')
        return

    for concert in concerts:
        name = concert.find('h2', attrs={'class': 'Title-sc-5meihc-3 eOlfER'}).text
        date = concert.find('li', attrs={'class': 'DetailsItem-sc-5meihc-1 gzFGVO'}).text
        price = concert.find('span', attrs={'class': 'PriceBlock-bp958r-11 cNqIOh'}).text
        price = int(''.join(filter(str.isdigit, price)))
        pos = date.find(',')
        create_concert(name, reformat_date(date[:pos]), price)

    logger.info('Page successfully parsed')
