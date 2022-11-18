from datetime import date

from .models import Concert, db
from .city import get_city_by_abb


def add_many_concerts(data: list[dict[str]]) -> None:
    with db.atomic():
        Concert.insert_many(data).on_conflict_ignore(True).execute()


def get_concert_by_id(concert_id: int) -> Concert | None:
    return Concert.get_or_none(Concert.id == concert_id)


def get_concerts_by_city(city_abb: str) -> list[Concert] | None:
    return Concert.select().where(Concert.city == get_city_by_abb(city_abb)).order_by(Concert.date.desc())


def delete_concert_by_id(concert_id: int) -> None:
    query = get_concert_by_id(concert_id)
    if query:
        query.delete_instance()


def clean_outdated_concerts() -> None:
    concert_list = Concert.select().where(Concert.date < date.today())
    if concert_list:
        for concert in concert_list:
            delete_concert_by_id(concert.id)
