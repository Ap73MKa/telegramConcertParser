from datetime import datetime
from peewee import Model, DateField, IntegerField, PrimaryKeyField, ForeignKeyField, DateTimeField, SqliteDatabase,\
    CharField


db = SqliteDatabase('database.db')


class _BaseModel(Model):
    class Meta:
        database = db


class City(_BaseModel):
    abb = CharField(unique=True, primary_key=True, max_length=32)
    name = CharField(unique=True, max_length=16)
    simple_name = CharField(unique=True)


class User(_BaseModel):
    user_id = IntegerField(unique=True, primary_key=True)
    name = CharField()
    city_page = IntegerField(default=1)


class Concert(_BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()
    date = DateField()
    price = IntegerField()
    link = CharField(unique=True)
    city = ForeignKeyField(City, backref='city')
    add_time = DateTimeField(default=datetime.now)


class UserCity(_BaseModel):
    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='user')
    city = ForeignKeyField(City, backref='city')
    date = DateTimeField(default=datetime.now)


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
