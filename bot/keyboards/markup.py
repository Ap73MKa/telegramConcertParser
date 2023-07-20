from abc import ABC
from math import ceil

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.database.models import User
from bot.database import get_all_cities_by_order_or_none, get_city_by_abb_or_none, get_all_city_of_user_or_none


class MarkupKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise "I am a static! Dont touch me..."

    @staticmethod
    def get_main(user: User) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        last_city = get_city_by_abb_or_none(get_all_city_of_user_or_none(user)[0].city_id)
        kb.add(
            KeyboardButton(text=f'Повторить запрос ({last_city.name}) ❤️‍🔥'),
            KeyboardButton(text='Предыдущие запросы 🔥'),
            KeyboardButton(text='Поиск концертов по городам 💥'),
            KeyboardButton(text='О телеграм боте 💬')
        )
        return kb

    @staticmethod
    def get_home() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        kb.add(KeyboardButton(text='Домой 🏚'))
        return kb

    @staticmethod
    def get_city_list(user: User, direction: int = 0) -> ReplyKeyboardMarkup:
        # todo: Think about this shit!
        kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        city_array = get_all_cities_by_order_or_none()
        page_available = ceil(len(city_array) / 9)

        tmp_count = user.city_page + direction
        if tmp_count <= 0:
            page_count = page_available
        elif tmp_count > page_available:
            page_count = tmp_count % page_available
        else:
            page_count = tmp_count

        user.city_page = page_count
        user.save()

        start_page = (page_count - 1) * 9
        cities = [city.name for city in city_array[start_page:start_page + 9]]

        for i in range(9 - len(cities)):
            cities.append('❌')

        for i in range(3):
            kb.add(*[KeyboardButton(text=cities[i * 3 + j]) for j in range(3)])

        kb.add(
            KeyboardButton(text='⬅️'),
            KeyboardButton(text=f'{page_count}/{page_available}\nДомой 🏚'),
            KeyboardButton(text='➡️')
        )

        return kb
