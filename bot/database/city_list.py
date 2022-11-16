from .models import City, UserCity
from .user import get_user_by_id


def create_city(abb: str, name: str) -> None:
    if not City.get_or_none(City.abb == abb):
        City.create(abb=abb, name=name)


def get_all_city() -> list[City] | None:
    return City.select()


def get_city_by_name(name: str) -> City | None:
    return City.get_or_none(City.city.name == name)


def get_city_by_abb(abb: str) -> City | None:
    return City.get_or_none(City.abb == abb)


def get_all_city_of_user(user_id: int) -> list[City] | None:
    user = get_user_by_id(user_id)
    if user:
        return UserCity.select().where(UserCity.user == user).order_by(UserCity.date)
    return None


def add_user_city(user_id: int, city_abb: str) -> None:
    city = get_city_by_abb(city_abb)
    user = get_user_by_id(user_id)
    all_cities = get_all_city_of_user(user_id)
    if len(all_cities) >= 8:
        pass
    old_city = UserCity.get_or_none(UserCity.city == city)
    if old_city:
        old_city.delete_instance()
    UserCity.create(user=user, city=city)
