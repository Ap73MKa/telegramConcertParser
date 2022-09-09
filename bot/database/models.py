from sqlalchemy import Column, Integer, Date, Text
from .main import Database


class Concert(Database.BASE):
    __tablename__ = 'CONCERT'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    date = Column(Date)
    price = Column(Integer)


def register_models():
    Database.BASE.metadata.create_all(Database().engine)
