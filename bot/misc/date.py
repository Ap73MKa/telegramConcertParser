from datetime import date


def reformat_date(start_day: str) -> date:
    months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
              'августа', 'сентября', 'октября', 'ноября', 'декабря')
    day, mon = start_day.split()
    mon = months.index(mon) + 1
    year = date.today().year
    if mon < date.today().month:
        year += 1
    return date(year, mon, int(day))
