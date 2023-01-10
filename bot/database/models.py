from datetime import datetime
from peewee import Model, DateField, IntegerField, PrimaryKeyField, ForeignKeyField, DateTimeField, SqliteDatabase,\
    CharField
from bot.modules import Config


db = SqliteDatabase(Config.DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class City(BaseModel):
    abb = CharField(unique=True, primary_key=True, max_length=32)
    name = CharField(unique=True, max_length=16)
    simple_name = CharField(unique=True)


class User(BaseModel):
    user_id = IntegerField(unique=True, primary_key=True)
    name = CharField()
    city_page = IntegerField(default=1)


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
