from time import perf_counter

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.database import Database

from src.bot.handlers.messages import Messages
from src.bot.handlers.states import MenuStates
from src.bot.keyboards import get_main_keyboard
from src.bot.middlewares import AdminFilter

# from src.bot.parser import create_concerts
from src.database.models import Concert

main_router = Router()
common_router = Router()


@main_router.message(CommandStart())
async def start_main_menu(message: Message, state: FSMContext, db: Database):
    user = await db.user.get(message.from_user.id)
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
    # await create_concerts()
    end_time = perf_counter()
    elapsed_time = start_time - end_time
    await message.answer(Messages.get_update_time(elapsed_time))


@main_router.message(MenuStates.main_menu, F.text.contains("O телеграм боте"))
async def handle_about_message(message: Message) -> None:
    await message.answer(Messages.get_site_info())


@main_router.message(MenuStates.main_menu, F.text.contains("Повторить запрос"))
async def handle_repeat_message(message: Message, db: Database) -> None:
    user = await db.user.get(message.from_user.id)
    user_cities = await db.user_city.get_cities_of_user(user.user_id)
    last_city = user_cities[0] if len(user_cities) >= 1 else None
    concerts = await db.concert.get_many(
        Concert.city_id == last_city.id,
        limit=20,
        order_by=Concert.concert_date)
    await message.answer(Messages.get_concert_list(concerts, last_city))


@main_router.message(F.text.contains("Домой"))
async def switch_to_main_menu_if_home(
    message: Message, state: FSMContext, db: Database
):
    await state.set_state(MenuStates.main_menu)
    await start_main_menu(message, state, db)


@common_router.message(F.text)
async def handle_unmatched_message(message: Message, state: FSMContext, db: Database):
    if not await state.get_state():
        await send_welcome_message(message, db)
        return
    await message.answer(
        "Извините, но я не понимаю ваше сообщение. Выберите пункт из меню."
    )


async def send_welcome_message(message: Message, db: Database):
    cities = await db.city.get_many()
    await message.answer_photo(
        photo="https://telegra.ph/file/188d44d07bf6497964b69.jpg",
        caption=Messages.get_bot_info(cities),
    )
