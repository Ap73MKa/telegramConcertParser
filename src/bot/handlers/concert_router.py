from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database.database import Database

from src.bot.handlers.main_router import main_router
from src.bot.handlers.messages import Messages
from src.bot.handlers.states import MenuStates
from src.bot.keyboards import get_home_keyboard, get_inline_city_keyboard
from src.database.models import City, Concert

concert_router = Router()


@concert_router.message(Command("start"))
async def start_concert_menu(message: Message, state: FSMContext, db: Database) -> None:
    user = await db.user.get(message.from_user.id)
    cities = await db.user_city.get_cities_of_user(user.user_id)
    await message.answer(text="Ваш список запросов:", reply_markup=get_home_keyboard())
    await message.answer(
        text=Messages.get_before_list(), reply_markup=get_inline_city_keyboard(cities)
    )
    await state.set_state(MenuStates.concert_menu)


@concert_router.message(MenuStates.concert_menu, F.text.contains("Просмотреть список"))
async def handle_recheck_list(message: Message, db: Database):
    user = await db.user.get(message.from_user.id)
    cities = await db.user_city.get_cities_of_user(user.user_id)
    await message.answer(
        text=Messages.get_before_list(), reply_markup=get_inline_city_keyboard(cities)
    )


@concert_router.callback_query(MenuStates.concert_menu, F.data.startswith("city-"))
async def handle_city_callback(query: CallbackQuery, db: Database):
    user = await db.user.get(query.from_user.id)
    data = query.data.split("-")
    if len(data) < 2:
        return None
    city_abb = data[1]
    city = await db.city.get_by_where(City.abb == city_abb)
    if not city:
        return None
    await db.user_city.new(user.user_id, city.id)
    concerts = await db.concert.get_many(
        Concert.city_id == city.id,
        limit=20,
        order_by=Concert.concert_date)
    await query.message.edit_text(Messages.get_concert_list(concerts, city))


@main_router.message(MenuStates.main_menu, F.text.contains("Предыдущие запросы"))
async def switch_to_concert_menu(message: Message, state: FSMContext, db: Database):
    await start_concert_menu(message, state, db)
