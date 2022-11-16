from .models import User


def get_user_by_id(user_id: int) -> User | None:
    return User.get_or_none(User.user_id == user_id)


def create_user(user_id: int) -> None:
    if not get_user_by_id(user_id):
        User.create(user_id=user_id)
