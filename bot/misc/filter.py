from aiogram.filters import Filter
from aiogram.types import Message

from bot.misc.utils import fuzzy_recognize_city


class FuzzyFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            _ = fuzzy_recognize_city(message.text)
            return True
        except ValueError:
            return False
