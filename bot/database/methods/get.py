from sqlalchemy import exc
from ..main import Database
from ..models import Concert


def get_concert_by_id(concert_id: int) -> Concert | None:
    try:
        return Database().session.query(Concert).filter(Concert.id == concert_id).one()
    except exc.NoResultFound:
        return None


def get_all_concerts() -> list[Concert] | None:
    try:
        return Database().session.query(Concert).order_by(Concert.date.desc()).all()
    except exc.NoResultFound:
        return None
