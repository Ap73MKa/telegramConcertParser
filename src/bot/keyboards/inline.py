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


def get_nav_city_inline_keyboard(
    city_abb: str, current_page: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text="Предыдущая страница",
            callback_data=f"navcity-{city_abb}-{current_page - 1}",
        ),
        InlineKeyboardButton(
            text="Следующая страница",
            callback_data=f"navcity-{city_abb}-{current_page + 1}",
        ),
    ]
    builder.add(*buttons)
    return builder.as_markup()
