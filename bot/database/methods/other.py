from datetime import date

from .get import get_all_concerts
from .delete import delete_concert_by_id


def clean_outdated_concerts() -> None:
    today_date = date.today()
    for concert in list(filter(lambda x: x.date < today_date, get_all_concerts())):
        delete_concert_by_id(concert.id)
