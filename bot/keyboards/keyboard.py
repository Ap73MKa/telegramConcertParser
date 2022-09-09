from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(KeyboardButton(text="Узнать концерты 🔥"))
    kb.add(KeyboardButton(text="Обновить базу данных ⚙"))
    return kb
