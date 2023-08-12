from collections.abc import Sequence
from math import ceil

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.models import City

CITIES_PER_PAGE = 9
HOME_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Просмотреть список 🔥")],
        [KeyboardButton(text="Домой 🏚")],
    ],
    resize_keyboard=True,
)


def get_home_keyboard() -> ReplyKeyboardMarkup:
    return HOME_KEYBOARD


def get_main_keyboard(last_city: City | None = None) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    if last_city:
        builder.row(KeyboardButton(text=f"Повторить запрос ({last_city.name}) ❤️‍🔥"))
        builder.row(KeyboardButton(text="Предыдущие запросы 🔥"))
    builder.row(KeyboardButton(text="Поиск концертов по городам 💥"))
    builder.row(KeyboardButton(text="O телеграм боте 💬"))
    return builder.as_markup()


def get_city_keyboard(cities: Sequence[City], current_page: int) -> ReplyKeyboardMarkup:
    max_pages = ceil(len(cities) / CITIES_PER_PAGE)
    start_page = (current_page - 1) * CITIES_PER_PAGE
    cities_on_page = cities[start_page : start_page + CITIES_PER_PAGE]
    cities_on_page = [city.name for city in cities_on_page]

    builder = ReplyKeyboardBuilder()
    builder.add(*_create_city_buttons(cities_on_page))
    builder.add(*_create_navigation_buttons(current_page, max_pages))
    builder.adjust(3, repeat=True)
    return builder.as_markup()


def _create_navigation_buttons(
    current_page: int, num_pages: int
) -> Sequence[KeyboardButton]:
    return [
        KeyboardButton(text="⬅️"),
        KeyboardButton(text=f"{current_page}/{num_pages}\nДомой 🏚"),
        KeyboardButton(text="➡️"),
    ]


def _create_city_buttons(city_list: Sequence[str]) -> Sequence[KeyboardButton]:
    buttons = [KeyboardButton(text=city) for city in city_list]
    buttons += [KeyboardButton(text="❌")] * (CITIES_PER_PAGE - len(buttons))
    return buttons
