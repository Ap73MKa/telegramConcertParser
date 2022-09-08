import requests as r

from bs4 import BeautifulSoup
from loguru import logger


def get_test_page():
    site = 'https://www.vladimirkoncert.ru/shows'
    concert_info = parse_page(r.get(site).text)
    logger.info('Page received successfully')
    return formate_list(concert_info)


def parse_page(page: str):
    result = []
    soup = BeautifulSoup(page, 'lxml')
    concerts = soup.find_all('div', {'class': 'show-descr'})
    for concert in concerts:
        performer = concert.find('div').text
        date = concert.find('h5').text
        result.append({
            'performer': performer,
            'date': date
        })
    return result


def formate_list(concert_list: list):
    string = ''
    for count, item in enumerate(concert_list):
        string += f'{count}. {item["performer"]} {item["date"]}\n'
        if count > 50:
            break
    return string
