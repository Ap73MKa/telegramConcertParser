from .models import User


def get_user_by_id(telegram_id: int) -> User | None:
    return User.get_or_none(User.telegram_id == telegram_id)


def create_user(telegram_id: int) -> None:
    if not get_user_by_id(telegram_id):
        User(telegram_id=telegram_id).save()


def add_city_to_user(telegram_id: int, city_abb: str) -> None:
    user = get_user_by_id(telegram_id)
    cities = user.cities.split(sep="||")
    if city_abb in cities:
        cities.remove(city_abb)
    cities.insert(0, city_abb)
    user.cities = "||".join(cities[:8])
    user.save()
