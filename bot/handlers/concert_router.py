from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery

from bot.database import get_all_city_of_user, get_user_by_id, create_user_city
from bot.handlers.main_router import start_main_menu, main_router
from bot.handlers.states import MenuStates
from bot.keyboards import MarkupKb, InlineKb
from bot.misc import Messages

concert_router = Router()


@concert_router.message(Command("start"))
async def start_concert_menu(message: Message, state: FSMContext) -> None:
    user = get_user_by_id(message.from_user.id)
    cities = [city.city_id.abb for city in get_all_city_of_user(user)]
    await message.answer("Ваш список запросов:", reply_markup=MarkupKb.get_home())
    await message.answer(
        Messages.get_before_list(), reply_markup=InlineKb.get_city(cities)
    )
    await state.set_state(MenuStates.concert_menu)


@concert_router.callback_query(MenuStates.concert_menu, F.data.startswith("city-"))
async def handle_city_callback(query: CallbackQuery):
    city_abb = query.data.split("-")[1]
    user = get_user_by_id(query.from_user.id)
    create_user_city(user, city_abb)
    await query.message.answer(Messages.get_concert_list(city_abb))


@main_router.message(MenuStates.main_menu, F.text.contains("Предыдущие запросы"))
async def switch_to_concert_menu(message: Message, state: FSMContext):
    await start_concert_menu(message, state)
