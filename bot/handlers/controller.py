from aiogram import Dispatcher

from bot.handlers.city_router import city_router
from bot.handlers.concert_router import concert_router
from bot.handlers.main_router import main_router, common_router


def register_handlers(dp: Dispatcher):
    main_router.include_routers(city_router, concert_router, common_router)
    dp.include_router(main_router)
