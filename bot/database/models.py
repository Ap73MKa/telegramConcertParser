from sqlalchemy import Column, Integer, Text, Date
from .main import Database


class Concert(Database.BASE):
    __tablename__ = 'CONCERT'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    date = Column(Date)
    price = Column(Integer)
    city = Column(Text)
    url = Column(Text)


def register_models() -> None:
    Database.BASE.metadata.create_all(Database().engine)
