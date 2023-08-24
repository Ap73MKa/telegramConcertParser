from aiogram.filters import Filter
from aiogram.types import Message
from config import configure


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == configure.bot.admin_id:
            return True
        return False
