from aiogram import Dispatcher
from aiogram.types import BotCommand

from src.bot.handlers.city_router import city_router
from src.bot.handlers.concert_router import concert_router
from src.bot.handlers.main_router import common_router, main_router
from src.bot.middlewares import DatabaseMiddleware, RegisterMiddleware

bot_commands = [BotCommand(command="/start", description="Начало работы с ботом")]


def register_handlers(dp: Dispatcher):
    main_router.include_routers(concert_router, city_router, common_router)
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(RegisterMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(RegisterMiddleware())
    dp.include_router(main_router)
