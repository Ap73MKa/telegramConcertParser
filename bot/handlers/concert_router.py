from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database import create_user_city, get_all_city_of_user, get_user_by_id_or_none
from bot.handlers.main_router import main_router
from bot.handlers.states import MenuStates
from bot.keyboards import InlineKb, MarkupKb
from bot.misc import Messages

concert_router = Router()


@concert_router.message(Command("start"))
async def start_concert_menu(message: Message, state: FSMContext) -> None:
    if not message.from_user or not (
        user := get_user_by_id_or_none(message.from_user.id)
    ):
        return None
    cities = [city.city_id.abb for city in get_all_city_of_user(user)]
    await message.answer("Ваш список запросов:", reply_markup=MarkupKb.get_home())
    await message.answer(
        Messages.get_before_list(), reply_markup=InlineKb.get_city(cities)
    )
    await state.set_state(MenuStates.concert_menu)


@concert_router.callback_query(MenuStates.concert_menu, F.data.startswith("city-"))
async def handle_city_callback(query: CallbackQuery):
    if not query.message or not query.data:
        return None
    if not (user := get_user_by_id_or_none(query.from_user.id)):
        return None
    data = query.data.split("-")
    if len(data) <= 1:
        return None
    city_abb = data[1]
    create_user_city(user, city_abb)
    await query.message.answer(Messages.get_concert_list(city_abb))


@main_router.message(MenuStates.main_menu, F.text.contains("Предыдущие запросы"))
async def switch_to_concert_menu(message: Message, state: FSMContext):
    await start_concert_menu(message, state)
