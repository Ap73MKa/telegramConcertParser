from peewee import Model, TextField, DateField, IntegerField, PrimaryKeyField
from .main import db


class BaseModel(Model):
    class Meta:
        database = db


class Concert(Model):
    id = PrimaryKeyField(null=False)
    name = TextField()
    date = DateField()
    price = IntegerField()
    city = TextField()
    url = TextField()

    class Meta:
        database = db


def register_models() -> None:
    for model in Model.__subclasses__():
        model.create_table()
