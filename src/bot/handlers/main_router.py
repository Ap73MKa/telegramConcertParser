from time import perf_counter

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from bot.handlers.common import get_answer_for_concert_keyboard
from bot.handlers.messages import Messages
from bot.handlers.states import MenuStates
from bot.keyboards import get_main_keyboard
from bot.middlewares import AdminFilter
from parser.controller import parse_api

from src.database import City, Database

# from src.bot.parser import create_concerts

main_router = Router()
common_router = Router()


@main_router.message(CommandStart())
async def start_main_menu(message: Message, state: FSMContext, db: Database):
    user_id = message.from_user.id  # type: ignore
    user = await db.user.get(user_id)
    user_cities = await db.user_city.get_cities_of_user(user.user_id)
    last_city = user_cities[0] if len(user_cities) >= 1 else None
    await message.answer(
        text=Messages.get_welcome(user_name=user.full_name),
        reply_markup=get_main_keyboard(last_city),
    )
    await state.set_state(MenuStates.main_menu)


@main_router.message(Command("update"), AdminFilter())
async def handle_update_command(message: Message, db: Database) -> None:
    start_time = perf_counter()
    await db.concert.delete_outdated()
    await parse_api(db)
    end_time = perf_counter()
    elapsed_time = end_time - start_time
    await message.answer(Messages.get_update_time(elapsed_time))


@main_router.message(MenuStates.main_menu, F.text.contains("O телеграм боте"))
async def handle_about_message(message: Message) -> None:
    await message.answer(Messages.SITE_INFO)


@main_router.message(MenuStates.main_menu, F.text.contains("Повторить запрос"))
async def handle_repeat_message(message: Message, db: Database) -> None:
    user_id = message.from_user.id  # type: ignore
    user = await db.user.get(user_id)
    user_cities = await db.user_city.get_cities_of_user(user.user_id)
    last_city = user_cities[0] if len(user_cities) >= 1 else None
    text, keyboard = await get_answer_for_concert_keyboard(1, last_city, db)
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


@main_router.message(F.text.contains("Домой"))
async def switch_to_main_menu_if_home(
    message: Message, state: FSMContext, db: Database
):
    await state.set_state(MenuStates.main_menu)
    await start_main_menu(message, state, db)


@main_router.callback_query(F.data.startswith("navcity-"))
async def handle_concert_navigation_callback(query: CallbackQuery, db: Database):
    data = query.data.split("-")  # type: ignore

    if len(data) < 3:
        return None
    city_abb = data[1]
    if not (city := await db.city.get_by_where(City.abb == city_abb)):
        return None
    page_numb = int(data[2])

    text, keyboard = await get_answer_for_concert_keyboard(page_numb, city, db)
    try:
        await query.message.edit_text(
            text, reply_markup=keyboard, disable_web_page_preview=True
        )
    except TelegramBadRequest:
        return None


@common_router.message(F.text)
async def handle_unmatched_message(message: Message, state: FSMContext, db: Database):
    if not await state.get_state():
        await send_welcome_message(message, db)
        return
    await message.answer(Messages.ERR_MAIN_MENU)


async def send_welcome_message(message: Message, db: Database):
    cities = await db.city.get_many()
    await message.answer_photo(
        photo="https://telegra.ph/file/188d44d07bf6497964b69.jpg",
        caption=Messages.get_bot_info(cities),
    )
