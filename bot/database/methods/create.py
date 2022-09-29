from datetime import date
from sqlalchemy import exc
from ..main import Database
from ..models import Concert


def create_concert(name: str, start_date: date, price: int, city: str, url: str) -> None:
    session = Database().session
    try:
        session.query(Concert.name).filter(Concert.name == name).one()
    except exc.NoResultFound:
        session.add(Concert(name=name, date=start_date, price=price, city=city, url=url))
        session.commit()
