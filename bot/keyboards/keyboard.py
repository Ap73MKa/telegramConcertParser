from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(
        KeyboardButton(text='Узнать концерты 🔥'),
        KeyboardButton(text='Обновить базу данных ⚙')
    )
    return kb


def get_city_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(text='test1', callback_data='test1'),
        InlineKeyboardButton(text='test2', callback_data='test2')
    )
    return kb
