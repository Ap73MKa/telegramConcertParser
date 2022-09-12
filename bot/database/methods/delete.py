from bot.database.main import Database
from bot.database.methods.get import get_concert_by_id


def delete_concert_by_id(concert_id: int) -> None:
    session = Database().session
    concert = get_concert_by_id(concert_id)
    if concert and concert.session:
        session.delete(concert.session)
        session.commit()
