from peewee import SqliteDatabase
from bot.modules import Config


db = SqliteDatabase(Config.DATABASE)
