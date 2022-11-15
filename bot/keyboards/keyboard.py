from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.modules import get_cities


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        KeyboardButton(text='Узнать концерты 🔥'),
        KeyboardButton(text='Узнать сайт 💬')
    )
    return kb


def get_city_keyboard(city_abb_list: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for abb in city_abb_list:
        kb.add(InlineKeyboardButton(text=get_cities()[abb], callback_data=f'city-{abb}'))
    return kb
