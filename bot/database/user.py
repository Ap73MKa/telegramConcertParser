from .models import User
from .city import add_user_city


def get_user_by_id(user_id: int) -> User | None:
    return User.get_or_none(User.user_id == user_id)


def create_user(user_id: int, name: str) -> None:
    if not get_user_by_id(user_id):
        User.create(user_id=user_id, name=name)
        user = get_user_by_id(user_id)
        add_user_city(user, 'spb')
        add_user_city(user, 'msk')
