from .models import City, UserCity, db, User


# region Sql create

def create_city(abb: str, name: str) -> None:
    if not City.get_or_none(City.abb == abb):
        City.create(abb=abb, name=name)


def create_user_city(user: User, city_abb: str) -> None:
    city = get_city_by_abb_or_none(city_abb)
    all_cities = get_all_city_of_user_or_none(user)

    if len(all_cities) >= 8:
        trash = all_cities[-1]
        trash.delete_instance()

    old_city = UserCity.get_or_none(UserCity.city == city)
    if old_city:
        old_city.delete_instance()
    UserCity.create(user=user, city=city)


# endregion

# region Sql get

def get_city_by_abb_or_none(abb: str) -> City | None:
    return City.get_or_none(City.abb == abb)


def get_all_cities_or_none() -> list[City] | None:
    return City.select()


def get_city_by_name_or_none(name: str) -> City | None:
    return City.get_or_none(City.simple_name == name)


def get_all_cities_by_order_or_none() -> list[City] | None:
    return City.select().order_by(City.name)


def get_all_city_of_user_or_none(user: User) -> list[City] | None:
    if user:
        return UserCity.select().where(UserCity.user == user).order_by(UserCity.date.desc())
    return None


# endregion

# region Sql insert

def insert_many_cities(data: list[dict[str, str]]) -> None:
    with db.atomic():
        City.insert_many(data).on_conflict_ignore(True).execute()

# endregion
