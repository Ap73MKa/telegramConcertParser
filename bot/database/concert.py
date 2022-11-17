from datetime import date

from .models import Concert


def create_concert(name: str, start_date: date, price: int, city: str, url: str) -> None:
    if not Concert.get_or_none(Concert.name == name):
        Concert.create(name=name, date=start_date, price=price, city=city, url=url)


def get_concert_by_id(concert_id: int) -> Concert | None:
    return Concert.get_or_none(Concert.id == concert_id)


def get_concerts_by_city(city_abb: str) -> list[Concert] | None:
    return Concert.select().where(Concert.city == city_abb).order_by(Concert.date.desc())


def delete_concert_by_id(concert_id: int) -> None:
    query = get_concert_by_id(concert_id)
    if query:
        query.delete_instance()


def clean_outdated_concerts() -> None:
    concert_list = Concert.select().where(Concert.date < date.today())
    if concert_list:
        for concert in concert_list:
            delete_concert_by_id(concert.id)
