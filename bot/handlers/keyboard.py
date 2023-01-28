from math import ceil

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.city import get_city_by_abb, get_all_cities_by_order, get_all_city_of_user
from bot.database.models import User


def get_main_keyboard(user: User = None) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    last_city = get_city_by_abb(get_all_city_of_user(user)[0].city_id)
    kb.add(
        KeyboardButton(text=f'Повторить запрос ({last_city.name}) ❤️‍🔥'),
        KeyboardButton(text='Предыдущие запросы 🔥'),
        KeyboardButton(text='Поиск концертов по городам 💥'),
        KeyboardButton(text='О телеграм боте 💬')
    )
    return kb


def get_city_keyboard(city_abb_list: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for abb in city_abb_list:
        kb.add(InlineKeyboardButton(text=get_city_by_abb(abb).name, callback_data=f'city-{abb}'))
    return kb


def get_home_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(KeyboardButton(text='Домой 🏚'))
    return kb


def get_city_list_keyboard(user: User, direction: int = 0) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    city_array = get_all_cities_by_order()
    page_available = ceil(len(city_array) / 9)

    page_count = user.city_page + direction
    page_count = page_available if page_count <= 0\
        else page_count % page_available if page_count > page_available else page_count

    user.city_page = page_count
    user.save()

    start_page = (page_count - 1) * 9
    cities = [city.name for city in city_array[start_page:start_page + 9]]

    for i in range(9 - len(cities)):
        cities.append('❌')

    for i in range(3):
        kb.add(
            KeyboardButton(text=cities[i * 3]),
            KeyboardButton(text=cities[i * 3 + 1]),
            KeyboardButton(text=cities[i * 3 + 2])
        )

    kb.add(KeyboardButton(text='⬅️'),
           KeyboardButton(text=f'{page_count}/{page_available}\nДомой 🏚'),
           KeyboardButton(text='➡️'))

    return kb
