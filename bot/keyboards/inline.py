from abc import ABC

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database import get_city_by_abb_or_none


class InlineKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise Exception("I am a static! Dont touch me...")

    @staticmethod
    def get_city(city_abb_list: list[str]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for abb in city_abb_list:
            if not (city := get_city_by_abb_or_none(abb)):
                continue
            button = InlineKeyboardButton(
                text=str(city.name), callback_data=f"city-{abb}"
            )
            builder.row(button)
        return builder.as_markup()
