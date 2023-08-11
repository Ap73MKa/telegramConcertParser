from aiogram.filters import Filter
from aiogram.types import Message
from database.database import Database


class FuzzyFilter(Filter):
    async def __call__(self, message: Message, db: Database) -> bool:
        return bool(await db.city.fuzzy_get_by_name(message.text))
