import sqlalchemy.exc

from bot.database.main import Database
from bot.database.models import Concert


def get_concert_by_name(name: str):
    try:
        return Database().session.query(Concert).filter(Concert.name == name).one()
    except sqlalchemy.exc.NoResultFound:
        return None
