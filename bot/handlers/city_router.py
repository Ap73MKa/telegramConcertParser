from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import get_user_by_id, create_user_city
from bot.handlers.main_router import main_router
from bot.handlers.states import MenuStates
from bot.keyboards import MarkupKb
from bot.misc import fuzzy_recognize_city, Messages

city_router = Router()


@city_router.message(Command("start"))
async def start_city_menu(message: Message, state: FSMContext):
    user = get_user_by_id(message.from_user.id)
    await message.answer(message.text, reply_markup=MarkupKb.get_city_list(user))
    await state.set_state(MenuStates.city_menu)


@main_router.message(MenuStates.city_menu, F.text.in_({"⬅️", "➡️"}))
async def handle_pagination_buttons(message: Message):
    emoji = message.text
    user = get_user_by_id(message.from_user.id)
    direction = -1 if emoji == "⬅️" else 1
    await message.answer(
        text=emoji, reply_markup=MarkupKb.get_city_list(user, direction)
    )


@main_router.message(MenuStates.city_menu, F.text)
async def handle_city_request_message(message: Message):
    try:
        city = fuzzy_recognize_city(message.text)
        user = get_user_by_id(message.from_user.id)
        create_user_city(user, city.abb)
        await message.answer(Messages.get_concert_list(city.abb))
    except ValueError:
        await message.answer("Неправильный ввод")


@main_router.message(
    MenuStates.main_menu, F.text.contains("Поиск концертов по городам")
)
async def switch_to_city_menu(message: Message, state: FSMContext):
    await start_city_menu(message, state)
