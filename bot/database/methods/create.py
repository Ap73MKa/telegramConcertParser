import sqlalchemy.exc

from bot.database.main import Database
from bot.database.models import Concert
from datetime import date


def create_concert(name: str, start_date: date, price: int) -> None:
    session = Database().session
    try:
        session.query(Concert.name).filter(Concert.name == name).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(Concert(name=name, date=start_date, price=price))
        session.commit()
