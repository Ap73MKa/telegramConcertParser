from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.data_structure import TransferData
from src.database.models import User


class RegisterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        db = data["db"]
        user = await db.user.get_by_where(User.user_id == event.from_user.id)
        if not user:
            await db.user.new(
                user_id=event.from_user.id, user_name=event.from_user.full_name
            )
        return await handler(event, data)
