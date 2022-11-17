from datetime import datetime
from peewee import Model, TextField, DateField, IntegerField, PrimaryKeyField, ForeignKeyField, DateTimeField,\
    SqliteDatabase
from bot.modules.config import Config


db = SqliteDatabase(Config.DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class City(BaseModel):
    abb = TextField()
    name = TextField()


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(unique=True)


class Concert(BaseModel):
    id = PrimaryKeyField(null=False)
    name = TextField()
    date = DateField()
    price = IntegerField()
    city = TextField()
    url = TextField()


class UserCity(BaseModel):
    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='user')
    city = ForeignKeyField(City, backref='city')
    date = DateTimeField(default=datetime.now)


def register_models() -> None:
    for model in BaseModel.__subclasses__():
        model.create_table()
