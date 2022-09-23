from datetime import date


def reformat_date(concert_date: str) -> date:
    months = ('Янв.', 'Февр.', 'Март', 'Апр.', 'Май', 'Июнь',
              'Июль', 'Авг.', 'Сент.', 'Окт.', 'Нояб.', 'Дек.')
    concert_date = concert_date.split()
    mon = months.index(concert_date[1]) + 1
    year = date.today().year
    year += 1 if mon < date.today().month else 0
    return date(year, mon, int(concert_date[0]))


def reformat_price(price: str) -> int:
    pos = price.find('—')
    price = price[:pos] if pos != 0 else price
    return int(''.join(filter(str.isdigit, price)))


def get_cities():
    return {
        'msk': 'Москва',
        'spb': 'Санкт-Петербург',
        'nn': 'Нижний Новгород',
        'rnd': 'Ростов-на-Дону',
        'kzn': 'Казань',
        'vlm': 'Владимир'
    }
