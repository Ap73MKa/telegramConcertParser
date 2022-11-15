from peewee import Model, TextField, DateField, IntegerField, PrimaryKeyField

from .main import db


class BaseModel(Model):
    class Meta:
        database = db


class Concert(BaseModel):
    id = PrimaryKeyField(null=False)
    name = TextField()
    date = DateField()
    price = IntegerField()
    city = TextField()
    url = TextField()


# todo CityList and List models (many-to-many relationships)
class User(BaseModel):
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(unique=True)
    cities = TextField(default="msk||spb")


def register_models() -> None:
    for model in BaseModel.__subclasses__():
        model.create_table()
