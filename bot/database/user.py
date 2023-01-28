from .city import create_user_city
from .models import User


# region Sql get

def get_user_by_id_or_none(user_id: int) -> User | None:
    return User.get_or_none(User.user_id == user_id)

# endregion


# region Sql create

def create_user(user_id: int, name: str) -> None:
    if not get_user_by_id_or_none(user_id):
        User.create(user_id=user_id, name=name)
        user = get_user_by_id_or_none(user_id)
        create_user_city(user, 'spb')
        create_user_city(user, 'msk')

# endregion
