from ..main import Database
from .get import get_concert_by_id


def delete_concert_by_id(concert_id: int) -> None:
    session = Database().session
    concert = get_concert_by_id(concert_id)
    if concert:
        session.delete(concert)
        session.commit()
