from datetime import date

from .models import Concert, db
from .city import get_city_by_abb_or_none


# region Sql get

def get_concert_by_id_or_none(concert_id: int) -> Concert | None:
    return Concert.get_or_none(Concert.id == concert_id)


def get_concerts_by_city_or_none(city_abb: str) -> list[Concert] | None:
    return Concert.select().where(Concert.city == get_city_by_abb_or_none(city_abb)).order_by(Concert.date.desc())


# endregion

# region Sql delete

def delete_concert_by_id(concert_id: int) -> None:
    # query = get_concert_by_id_or_none(concert_id)
    # if query:
    #     query.delete_instance()
    if query := get_concert_by_id_or_none(concert_id):
        query.delete_instance()


def delete_outdated_concerts() -> None:
    # concert_list = Concert.select().where(Concert.date < date.today())
    # if concert_list:
    #     for concert in concert_list:
    #         delete_concert_by_id(concert.id)
    if concert_list := Concert.select().where(Concert.date < date.today()):
        for concert in concert_list:
            delete_concert_by_id(concert.id)


# endregion

# region Sql insert

def insert_many_concerts(data: list[dict[str]]) -> None:
    with db.atomic():
        Concert.insert_many(data).on_conflict_ignore(True).execute()

# endregion
