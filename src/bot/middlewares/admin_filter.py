from aiogram.filters import Filter
from aiogram.types import Message


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return True
