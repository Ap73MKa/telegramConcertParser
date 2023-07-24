from abc import ABC
from math import ceil

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.database import (
    get_all_cities_by_order,
    get_all_city_of_user,
    get_city_by_abb_or_none,
)
from bot.database.models import User

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
        kb = []
        all_user_cities = get_all_city_of_user(user)
        if all_user_cities and (
            last_city := get_city_by_abb_or_none(all_user_cities[0].city_id)
        ):
            kb = [
                [KeyboardButton(text=f"Повторить запрос ({last_city.name}) ❤️‍🔥")],
                [KeyboardButton(text="Предыдущие запросы 🔥")],
            ]
        kb.extend(
            [
                [KeyboardButton(text="Поиск концертов по городам 💥")],
                [KeyboardButton(text="O телеграм боте 💬")],
            ]
        )
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    @staticmethod
    def get_home() -> ReplyKeyboardMarkup:
        kb = [[KeyboardButton(text="Домой 🏚")]]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    @staticmethod
    def get_city_list(user: User, direction: int = 0) -> ReplyKeyboardMarkup:
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
        kb = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
        kb.append(
            [
                KeyboardButton(text="⬅️"),
                KeyboardButton(text=f"{current_page}/{num_pages}\nДомой 🏚"),
                KeyboardButton(text="➡️"),
            ]
        )
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
