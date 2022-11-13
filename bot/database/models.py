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


def register_models() -> None:
    Concert.create_table()
