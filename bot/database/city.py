from .models import City, User, UserCity, db

# region Sql create


def create_city(abb: str, name: str) -> None:
    if not City.get_or_none(City.abb == abb):
        City.create(abb=abb, name=name)


def create_user_city(user: User, city_abb: str) -> None:
    city = get_city_by_abb_or_none(city_abb)
    all_cities = get_all_city_of_user(user)
    max_city_count = 8

    if len(all_cities) >= max_city_count:
        trash = all_cities[-1]
        trash.delete_instance()

    old_city = UserCity.get_or_none(UserCity.city_id == city)
    if old_city:
        old_city.delete_instance()
    UserCity.create(user_id=user, city_id=city)


# endregion

# region Sql get


def get_city_by_abb_or_none(abb: str) -> City | None:
    return City.get_or_none(City.abb == abb)


def get_city_by_name_or_none(name: str) -> City | None:
    return City.get_or_none(City.simple_name == name)


def get_all_cities() -> list[City]:
    return City.select()


def get_all_cities_by_order() -> list[City]:
    return City.select().order_by(City.name)


def get_all_city_of_user(user: User) -> list[UserCity]:
    return (
        UserCity.select().where(UserCity.user_id == user).order_by(UserCity.date.desc())
    )


# endregion

# region Sql insert


def insert_many_cities(data: list[dict[str, str]]) -> None:
    with db.atomic():
        City.insert_many(data).on_conflict_ignore(True).execute()


# endregion
