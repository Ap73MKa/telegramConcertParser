import sqlalchemy.exc

from bot.database.main import Database
from bot.database.models import Concert


def get_concert_by_id(concert_id: int) -> Concert | None:
    try:
        return Database().session.query(Concert).filter(Concert.id == concert_id).one()
    except sqlalchemy.exc.NoResultFound:
        return None


def get_all_concerts() -> list[Concert] | None:
    try:
        return Database().session.query(Concert).order_by(Concert.date.desc()).all()
    except sqlalchemy.exc.NoResultFound:
        return None
