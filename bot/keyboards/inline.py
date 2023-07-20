from abc import ABC

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database import get_city_by_abb_or_none


class InlineKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise "I am a static! Dont touch me..."

    @staticmethod
    def get_city(city_abb_list: list[str]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(row_width=1)
        for abb in city_abb_list:
            kb.add(InlineKeyboardButton(text=get_city_by_abb_or_none(abb).name, callback_data=f'city-{abb}'))
        return kb
