from math import ceil

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.database.city import (
    get_city_by_abb,
    get_all_cities_by_order,
    get_all_city_of_user,
)
from bot.database.models import User


CITIES_PER_PAGE = 9


def get_main_keyboard(user: User = None) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    last_city = get_city_by_abb(get_all_city_of_user(user)[0].city_id)
    kb.add(
        KeyboardButton(text=f"Повторить запрос ({last_city.name}) ❤️‍🔥"),
        KeyboardButton(text="Предыдущие запросы 🔥"),
        KeyboardButton(text="Поиск концертов по городам 💥"),
        KeyboardButton(text="О телеграм боте 💬"),
    )
    return kb


def get_city_keyboard(city_abb_list: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for abb in city_abb_list:
        kb.add(
            InlineKeyboardButton(
                text=get_city_by_abb(abb).name, callback_data=f"city-{abb}"
            )
        )
    return kb


def get_home_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(KeyboardButton(text="Домой 🏚"))
    return kb


def __update_current_page(user: User, direction: int, num_pages: int) -> int:
    current_page = user.city_page + direction
    current_page = max(1, min(current_page, num_pages))
    user.city_page = current_page
    user.save()
    return current_page


def get_city_list_keyboard(user: User, direction: int = 0) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    city_list = get_all_cities_by_order()
    num_pages = ceil(len(city_list) / CITIES_PER_PAGE)
    current_page = __update_current_page(user, direction, num_pages)
    start_page = (current_page - 1) * CITIES_PER_PAGE
    cities = [
        city.name for city in city_list[start_page : start_page + CITIES_PER_PAGE]
    ]
    buttons = [KeyboardButton(text=city) for city in cities] + [
        KeyboardButton(text="❌")
    ] * (CITIES_PER_PAGE - len(cities))

    for i in range(0, len(buttons), 3):
        kb.add(*buttons[i : i + 3])

    kb.add(
        KeyboardButton(text="⬅️"),
        KeyboardButton(text=f"{current_page}/{num_pages}\nДомой 🏚"),
        KeyboardButton(text="➡️"),
    )

    return kb
