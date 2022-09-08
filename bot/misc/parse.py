import requests as r
from bs4 import BeautifulSoup

link = 'https://afisha.yandex.ru/vladimir/selections/all-events-concert'


def get_concert_list() -> str:
    return __formate_info(__parse_page(__get_request(link)))


def __get_request(site: str) -> str:
    return r.get(site).text


def __parse_page(page: str) -> list:
    soup = BeautifulSoup(page, 'lxml')
    concerts = soup.find_all('div', {'class': 'Inner-sc-5s87mw-1 fXrHG'})

    if not concerts:
        return []

    result = []
    for concert in concerts:
        name = concert.find('h2', attrs={'class': 'Title-sc-5meihc-3 eOlfER'}).text
        date = concert.find('li', attrs={'class': 'DetailsItem-sc-5meihc-1 gzFGVO'}).text
        price = concert.find('span', attrs={'class': 'PriceBlock-bp958r-11 cNqIOh'}).text
        pos = date.find(',')
        result.append({
            'name': name,
            'date': date[:pos],
            'price': price
        })

    return result


def __formate_info(concert_list: list) -> str:
    return '\n'.join([f'{count + 1}. {item["name"]} {item["date"]} {item["price"]}'
                      for count, item in enumerate(concert_list)])
