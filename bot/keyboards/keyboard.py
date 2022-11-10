from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.parsing import get_cities


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        KeyboardButton(text='Узнать концерты 🔥'),
        KeyboardButton(text='Узнать сайт 💬')
    )
    return kb


def get_city_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for abb, city in get_cities().items():
        kb.add(InlineKeyboardButton(text=city, callback_data=f'city-{abb}'))
    return kb
