from peewee import Model, TextField, DateField, IntegerField, PrimaryKeyField, ForeignKeyField

from .main import db


class BaseModel(Model):
    class Meta:
        database = db


class City(BaseModel):
    abb = TextField()
    name = TextField()


class UserCity(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField()
    city = ForeignKeyField(City, backref='city')


class Concert(BaseModel):
    id = PrimaryKeyField(null=False)
    name = TextField()
    date = DateField()
    price = IntegerField()
    city = TextField()
    url = TextField()


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(unique=True)
    # cities = ForeignKeyField(UserCity, backref='user-city')


def register_models() -> None:
    for model in BaseModel.__subclasses__():
        model.create_table()
