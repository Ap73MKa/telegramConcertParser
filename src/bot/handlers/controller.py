from aiogram import Dispatcher
from aiogram.types import BotCommand
from bot.handlers.city_router import city_router
from bot.handlers.concert_router import concert_router
from bot.handlers.main_router import common_router, main_router
from bot.middlewares import DatabaseMiddleware, RegisterMiddleware

bot_commands = [BotCommand(command="/start", description="Начало работы с ботом")]


def register_handlers(dp: Dispatcher):
    main_router.include_routers(city_router, concert_router, common_router)
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(RegisterMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(RegisterMiddleware())
    dp.include_router(main_router)
