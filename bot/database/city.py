from .models import City, UserCity, User, db


def create_city(abb: str, name: str) -> None:
    if not City.get_or_none(City.abb == abb):
        City.create(abb=abb, name=name)


def add_many_cities(data: list[dict[str, str]]) -> None:
    with db.atomic():
        City.insert_many(data).on_conflict_ignore(True).execute()


def get_all_cities() -> list[City] | None:
    return City.select()


def get_all_cities_by_order() -> list[City] | None:
    return City.select().order_by(City.name)


def get_city_by_name(name: str) -> City | None:
    return City.get_or_none(City.simple_name == name)


def get_city_by_abb(abb: str) -> City | None:
    return City.get_or_none(City.abb == abb)


def get_all_city_of_user(user: User) -> list[City] | None:
    if user:
        return (
            UserCity.select()
            .where(UserCity.user == user)
            .order_by(UserCity.date.desc())
        )
    return None


def add_user_city(user: User, city_abb: str) -> None:
    city = get_city_by_abb(city_abb)
    all_cities = get_all_city_of_user(user)

    if len(all_cities) >= 8:
        trash = all_cities[-1]
        trash.delete_instance()

    old_city = UserCity.get_or_none(UserCity.city == city)
    if old_city:
        old_city.delete_instance()
    UserCity.create(user=user, city=city)
