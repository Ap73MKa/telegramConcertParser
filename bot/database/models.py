from datetime import datetime
from peewee import Model, TextField, DateField, IntegerField, PrimaryKeyField, ForeignKeyField, DateTimeField,\
    SqliteDatabase, CharField
from bot.modules.config import Config


db = SqliteDatabase(Config.DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class City(BaseModel):
    abb = CharField(unique=True)
    name = CharField(unique=True)


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(unique=True)


class Concert(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()
    date = DateField()
    price = IntegerField()
    link = CharField(unique=True)
    city = ForeignKeyField(City, backref='city')
    add_time = DateTimeField(default=datetime.now)


class UserCity(BaseModel):
    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='user')
    city = ForeignKeyField(City, backref='city')
    date = DateTimeField(default=datetime.now)


def register_models() -> None:
    for model in BaseModel.__subclasses__():
        model.create_table()
