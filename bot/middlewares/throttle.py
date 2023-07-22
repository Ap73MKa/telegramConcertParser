from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.5, key_prefix: str = "antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super().__init__()

    async def on_process_message(self, message: Message, data: dict[str, str]) -> None:
        await self._throttle(message, data)

    async def on_process_callback_query(
        self, query: CallbackQuery, data: dict[str, str]
    ) -> None:
        await self._throttle(query.message, data)

    # pylint: disable=W0613
    async def _throttle(self, message: Message, data: dict[str, str]) -> None:
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(
                handler, "throttling_key", f"{self.prefix}_{handler.__name__}"
            )
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as throttled:
            if throttled.exceeded_count <= 2:
                await message.reply("Вы превысили число запросов 😕")
            raise CancelHandler() from throttled
