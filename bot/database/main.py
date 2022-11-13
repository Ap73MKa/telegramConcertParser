# from typing import Final
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
#
#
# class Database(metaclass=SingletonMeta):
#     BASE: Final = declarative_base()
#
#     def __init__(self):
#         self.__engine = create_engine('sqlite:///database.db')
#         session = sessionmaker(bind=self.__engine)
#         self.__session = session()
#
#     @property
#     def session(self):
#         return self.__session
#
#     @property
#     def engine(self):
#         return self.__engine


# from bot.modules.singleton import SingletonMeta
# import peewee
#
#
# class Database(metaclass=SingletonMeta):
#
#     def __init__(self):
#         self.__engine = peewee.SqliteDatabase('database.db')
#
#     @property
#     def engine(self):
#         return self.__engine
from peewee import SqliteDatabase


db = SqliteDatabase('database.db')
