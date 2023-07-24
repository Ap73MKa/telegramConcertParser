from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import create_user_city, get_user_by_id_or_none
from bot.handlers.main_router import main_router, start_main_menu
from bot.handlers.states import MenuStates
from bot.keyboards import MarkupKb
from bot.misc import FuzzyFilter, Messages, fuzzy_recognize_city

city_router = Router()


@city_router.message(Command("start"))
async def start_city_menu(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return None
    if not (user := get_user_by_id_or_none(message.from_user.id)):
        return None
    await message.answer(message.text, reply_markup=MarkupKb.get_city_list(user))
    await state.set_state(MenuStates.city_menu)


@city_router.message(MenuStates.city_menu, F.text.in_({"⬅️", "➡️"}))
async def handle_pagination_buttons(message: Message):
    if not message.text:
        return None
    if not message.from_user or not (
        user := get_user_by_id_or_none(message.from_user.id)
    ):
        return None
    emoji = message.text
    direction = -1 if emoji == "⬅️" else 1
    await message.answer(
        text=emoji, reply_markup=MarkupKb.get_city_list(user, direction)
    )

@city_router.message(MenuStates.city_menu, F.text.contains("❌"))
async def handle_empty_sticker(message: Message, state: FSMContext):
    await start_main_menu(message, state)


@city_router.message(MenuStates.city_menu, FuzzyFilter())
async def handle_city_request_message(message: Message):
    if not message.text:
        return None
    city = fuzzy_recognize_city(message.text)
    if not message.from_user or not (
        user := get_user_by_id_or_none(message.from_user.id)
    ):
        return None
    create_user_city(user, city.abb)
    await message.answer(Messages.get_concert_list(city.abb))


@main_router.message(
    MenuStates.main_menu, F.text.contains("Поиск концертов по городам")
)
async def switch_to_city_menu(message: Message, state: FSMContext):
    await start_city_menu(message, state)
