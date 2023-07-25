from abc import ABC

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database import get_city_by_abb_or_none


class InlineKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise Exception("I am a static! Dont touch me...")

    @staticmethod
    def get_city_keyboard(city_abb_list: list[str]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        buttons = [
            InlineKeyboardButton(
                text=str(get_city_by_abb_or_none(abb).name),
                callback_data=f"city-{abb}"
            )
            for abb in city_abb_list
            if get_city_by_abb_or_none(abb)
        ]
        builder.add(*buttons)
        builder.adjust(1, repeat=True)
        return builder.as_markup()
