from .models import User

# region Sql get


def get_user_by_id_or_none(user_id: int) -> User | None:
    return User.get_or_none(User.user_id == user_id)


# endregion


# region Sql create


def create_user(user_id: int, name: str = "User") -> None:
    if not get_user_by_id_or_none(user_id):
        User.create(user_id=user_id, name=name)


# endregion
