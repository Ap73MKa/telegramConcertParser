from datetime import date
from ..main import Database
from .get import get_all_concerts
from .delete import delete_concert_by_id


def clean_outdated_concerts() -> None:
    concerts = get_all_concerts()
    today_date = date.today()
    for concert in concerts:
        if concert.date < today_date:
            delete_concert_by_id(concert.id)
    Database().session.commit()
