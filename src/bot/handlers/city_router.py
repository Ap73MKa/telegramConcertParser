from math import ceil

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.database import Database

from src.bot.handlers.main_router import main_router, start_main_menu
from src.bot.handlers.messages import Messages
from src.bot.handlers.states import MenuStates
from src.bot.keyboards import CITIES_PER_PAGE, get_city_keyboard
from src.database.models import City, Concert

city_router = Router()


@city_router.message(CommandStart())
async def start_city_menu(message: Message, state: FSMContext, db: Database):
    user = await db.user.get(message.from_user.id)
    cities = await db.city.get_many(order_by=City.name)
    await message.answer(
        message.text, reply_markup=get_city_keyboard(cities, user.city_page)
    )
    await state.set_state(MenuStates.city_menu)


@city_router.message(MenuStates.city_menu, F.text.in_({"⬅️", "➡️"}))
async def handle_pagination_buttons(message: Message, db: Database):
    emoji = message.text
    direction = -1 if emoji == "⬅️" else 1
    user = await db.user.get(message.from_user.id)
    cities = await db.city.get_many(order_by=City.name)

    max_page_count = ceil(len(cities) / CITIES_PER_PAGE)
    current_page = max(1, min(user.city_page + direction, max_page_count))
    await db.user.update_page(user_id=user.user_id, page=current_page)

    await message.answer(
        text=emoji,
        reply_markup=get_city_keyboard(cities=cities, current_page=current_page),
    )


@city_router.message(MenuStates.city_menu, F.text.contains("❌"))
async def handle_empty_sticker(message: Message, state: FSMContext, db: Database):
    await start_main_menu(message, state, db)


@city_router.message(MenuStates.city_menu)
async def handle_city_request_message(message: Message, db: Database):
    if not (city := await db.city.fuzzy_get_by_name(message.text)):
        return None
    user = await db.user.get(message.from_user.id)
    concerts = await db.concert.get_many(
        Concert.city_id == city.id,
        limit=20,
        order_by=Concert.concert_date)
    await db.user_city.new(user.user_id, city.id)
    await message.answer(Messages.get_concert_list(concerts, city))


@main_router.message(
    MenuStates.main_menu, F.text.contains("Поиск концертов по городам")
)
async def switch_to_city_menu(message: Message, state: FSMContext, db: Database):
    await start_city_menu(message, state, db)
