from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from bot.handlers.common import get_answer_for_concert_keyboard
from bot.handlers.main_router import main_router
from bot.handlers.messages import Messages
from bot.handlers.states import MenuStates
from bot.keyboards import get_home_keyboard, get_inline_city_keyboard

from src.database import City, Database

concert_router = Router()


@concert_router.message(Command("start"))
async def start_concert_menu(message: Message, state: FSMContext, db: Database) -> None:
    user_id = message.from_user.id  # type: ignore
    user = await db.user.get(user_id)
    cities = await db.user_city.get_cities_of_user(user.user_id)
    await message.answer(text="Ваш список запросов:", reply_markup=get_home_keyboard())
    await message.answer(
        text=Messages.PREFACE_CONCERT_LIST,
        reply_markup=get_inline_city_keyboard(cities),
    )
    await state.set_state(MenuStates.concert_menu)


@concert_router.message(MenuStates.concert_menu, F.text.contains("Просмотреть список"))
async def handle_recheck_list(message: Message, db: Database):
    user_id = message.from_user.id  # type: ignore
    user = await db.user.get(user_id)
    cities = await db.user_city.get_cities_of_user(user.user_id)
    await message.answer(
        text=Messages.PREFACE_CONCERT_LIST,
        reply_markup=get_inline_city_keyboard(cities),
    )


@concert_router.callback_query(MenuStates.concert_menu, F.data.startswith("city-"))
async def handle_city_callback(query: CallbackQuery, db: Database):
    user_id = query.from_user.id  # type: ignore
    user = await db.user.get(user_id)
    data = query.data  # type: ignore
    city = await get_city_from_callback(data, db)
    if not city:
        return None
    await db.user_city.new(user.user_id, city.id)
    text, keyboard = await get_answer_for_concert_keyboard(1, city, db)
    await query.message.edit_text(text, reply_markup=keyboard, disable_web_page_preview=True)  # type: ignore


async def get_city_from_callback(data: str, db: Database) -> City | None:
    data_split = data.split("-")
    if len(data_split) < 2:
        return None
    city_abb = data_split[1]
    return await db.city.get_by_where(City.abb == city_abb)


@main_router.message(MenuStates.main_menu, F.text.contains("Предыдущие запросы"))
async def switch_to_city_menu(message: Message, state: FSMContext, db: Database):
    await start_concert_menu(message, state, db)
