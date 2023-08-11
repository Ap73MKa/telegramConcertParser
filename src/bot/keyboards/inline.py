from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import City


def get_inline_city_keyboard(cities: Sequence[City]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=city.name, callback_data=f"city-{city.abb}")
        for city in cities
    ]
    builder.add(*buttons)
    builder.adjust(1, repeat=True)
    return builder.as_markup()
