from .models import City, UserCity


def create_city(abb: str, name: str) -> None:
    if not City.get_or_none(City.abb == abb):
        City(abb=abb, name=name).save()


def get_all_city() -> list[City] | None:
    return City.select()


def get_city_by_name(name: str) -> City | None:
    return City.get_or_none(City.city.name == name)


def get_city_by_abb(abb: str) -> City | None:
    return City.get_or_none(City.city.abb == abb)


def add_user_city(user_id: int, city: City):
    if not UserCity.get_or_none(UserCity.city == city):
        UserCity(user_id=user_id, city=city)


def get_all_city_of_user(user_id: int) -> list[City] | None:
    return UserCity.select().where(UserCity.user_id == user_id)
