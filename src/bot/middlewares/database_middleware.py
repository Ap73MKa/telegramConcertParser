from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from bot.data_structure import TransferData
from database.database import Database


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        async with data["pool"]() as session:
            data["db"] = Database(session)
            await handler(event, data)
            await session.commit()
