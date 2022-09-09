from bot.database.main import Database
from bot.database.methods.get import get_concert_by_name


def delete_concert(name: str):
    session = Database().session
    concert = get_concert_by_name(name)
    if concert and concert.session:
        session.delete(concert.session)
        session.commit()
