import httpx

from loguru import logger
from bs4 import BeautifulSoup
from bot.database.methods.create import create_concert
from bot.database.methods.get import get_all_concerts
from user_agent import generate_user_agent
from .date import reformat_date
from fp.fp import FreeProxy


def get_concert_list() -> str:
    concert_list = reversed(get_all_concerts())
    return '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                      for concert in concert_list])


def update_database() -> None:
    url = 'https://afisha.yandex.ru/vladimir/selections/all-events-concert'
    __gather_info(__get_http(url))


def __get_http(url: str) -> str:
    try:
        header = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux')),
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        proxy = {'http://': FreeProxy(rand=True).get()}
        logger.info(f'Proxy is founded: {proxy["http://"][7:]}')
        with httpx.Client(headers=header, proxies=proxy, follow_redirects=True) as client:
            page_response = client.get(url, timeout=5)
        logger.info(f'Page status: {page_response.status_code}')
        return page_response.text
    except Exception as e:
        logger.error(str(e))
        return ''


def __gather_info(site: str) -> None:
    soup = BeautifulSoup(site, 'lxml')
    info_blocks = soup.find_all('div', {'class': 'Inner-sc-5s87mw-1 fXrHG'})

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
