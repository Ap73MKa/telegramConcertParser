from abc import ABC
from math import ceil

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.database.models import User
from bot.database import (
    get_all_cities_by_order,
    get_city_by_abb_or_none,
    get_all_city_of_user,
)

_CITIES_PER_PAGE = 9


def _update_current_page(user: User, direction: int, num_pages: int) -> int:
    current_page = user.city_page + direction
    current_page = max(1, min(current_page, num_pages))
    user.city_page = current_page
    user.save()
    return current_page


class MarkupKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise Exception("I am a static! Dont touch me...")

    @staticmethod
    def get_main(user: User) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        last_city = get_city_by_abb_or_none(get_all_city_of_user(user)[0].city_id)
        kb.add(
            KeyboardButton(text=f"Повторить запрос ({last_city.name}) ❤️‍🔥"),
            KeyboardButton(text="Предыдущие запросы 🔥"),
            KeyboardButton(text="Поиск концертов по городам 💥"),
            KeyboardButton(text="О телеграм боте 💬"),
        )
        return kb

    @staticmethod
    def get_home() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        kb.add(KeyboardButton(text="Домой 🏚"))
        return kb

    @staticmethod
    def get_city_list(user: User, direction: int = 0) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        city_list = get_all_cities_by_order()
        num_pages = ceil(len(city_list) / _CITIES_PER_PAGE)
        current_page = _update_current_page(user, direction, num_pages)
        start_page = (current_page - 1) * _CITIES_PER_PAGE
        cities = [
            city.name for city in city_list[start_page : start_page + _CITIES_PER_PAGE]
        ]
        buttons = [KeyboardButton(text=city) for city in cities] + [
            KeyboardButton(text="❌")
        ] * (_CITIES_PER_PAGE - len(cities))

        for i in range(0, len(buttons), 3):
            kb.add(*buttons[i : i + 3])

        kb.add(
            KeyboardButton(text="⬅️"),
            KeyboardButton(text=f"{current_page}/{num_pages}\nДомой 🏚"),
            KeyboardButton(text="➡️"),
        )

        return kb
