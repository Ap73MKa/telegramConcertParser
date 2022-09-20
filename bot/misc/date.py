from datetime import date


def reformat_date(start_day: str) -> date:
    months = ('Янв', 'Февр', 'Март', 'Апр.', 'Мая', 'Июня',
              'Июля', 'Авг', 'Сент', 'Окт', 'Нояб', 'Дек')

    day, mon = start_day.split()
    mon = months.index(mon) + 1
    year = date.today().year

    if mon < date.today().month:
        year += 1

    return date(year, mon, int(day))
