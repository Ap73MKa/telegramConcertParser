from math import ceil

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.database import (
    get_all_cities_by_order,
    get_all_city_of_user,
    get_city_by_abb_or_none,
)
from bot.database.models import User

_CITIES_PER_PAGE = 9


class MarkupKb:
    def __new__(cls, *args, **kwargs):
        raise Exception("I am a static! Dont touch me...")

    # region Private

    @staticmethod
    def _update_current_page(user: User, direction: int, num_pages: int) -> int:
        current_page = user.city_page + direction
        current_page = max(1, min(current_page, num_pages))
        user.city_page = current_page
        user.save()
        return current_page

    @staticmethod
    def _create_navigation_buttons(current_page: int, num_pages: int) -> list[KeyboardButton]:
        return [
            KeyboardButton(text="⬅️"),
            KeyboardButton(text=f"{current_page}/{num_pages}\nДомой 🏚"),
            KeyboardButton(text="➡️"),
        ]

    @staticmethod
    def _create_city_buttons(city_list: list[str]) -> list[KeyboardButton]:
        buttons = [KeyboardButton(text=city) for city in city_list]
        buttons += [KeyboardButton(text="❌")] * (_CITIES_PER_PAGE - len(buttons))
        return buttons

    # endregion

    # region Public

    @staticmethod
    def get_main_keyboard(user: User) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        all_user_cities = get_all_city_of_user(user)
        if all_user_cities and (
            last_city := get_city_by_abb_or_none(all_user_cities[0].city_id)
        ):
            builder.row(KeyboardButton(text=f"Повторить запрос ({last_city.name}) ❤️‍🔥"))
            builder.row(KeyboardButton(text="Предыдущие запросы 🔥"))
        builder.row(KeyboardButton(text="Поиск концертов по городам 💥"))
        builder.row(KeyboardButton(text="O телеграм боте 💬"))
        return builder.as_markup()

    @staticmethod
    def get_home_keyboard() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Просмотреть список 🔥"))
        builder.row(KeyboardButton(text="Домой 🏚"))
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_city_keyboard(user: User, direction: int = 0) -> ReplyKeyboardMarkup:
        city_list = get_all_cities_by_order()
        num_pages = ceil(len(city_list) / _CITIES_PER_PAGE)
        current_page = MarkupKb._update_current_page(user, direction, num_pages)
        start_page = (current_page - 1) * _CITIES_PER_PAGE
        cities_on_page = city_list[start_page : start_page + _CITIES_PER_PAGE]
        cities_on_page = [city.name for city in cities_on_page]

        builder = ReplyKeyboardBuilder()
        builder.add(*MarkupKb._create_city_buttons(cities_on_page))
        builder.add(*MarkupKb._create_navigation_buttons(current_page, num_pages))
        builder.adjust(3, repeat=True)
        return builder.as_markup()

    # endregion
