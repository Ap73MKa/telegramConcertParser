from time import perf_counter

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import (
    create_user,
    delete_outdated_concerts,
    get_all_city_of_user,
    get_user_by_id_or_none,
)
from bot.handlers.states import MenuStates
from bot.keyboards import MarkupKb
from bot.misc import Config, Messages
from bot.parsing import create_concerts

main_router = Router()
common_router = Router()


@main_router.message(Command("start"))
async def start_main_menu(message: Message, state: FSMContext):
    if not message.from_user:
        return None
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    create_user(user_id, user_name)
    if not (user := get_user_by_id_or_none(message.from_user.id)):
        return None
    await message.answer(
        Messages.get_welcome(user_name), reply_markup=MarkupKb.get_main(user)
    )
    await state.set_state(MenuStates.main_menu)


@main_router.message(Command("update"))
async def handle_update_command(message: Message) -> None:
    if not message.from_user:
        return None
    user_id = message.from_user.id
    if user_id != int(Config.ADMIN_ID):
        await message.answer("You don't have permission")
        return
    timer = perf_counter()
    delete_outdated_concerts()
    await create_concerts()
    final_time = Messages.get_update_time(perf_counter() - timer)
    await message.answer(final_time)


@main_router.message(MenuStates.main_menu, F.text.contains("O телеграм боте"))
async def handle_about_message(message: Message) -> None:
    await message.answer(Messages.get_site_info())


@main_router.message(MenuStates.main_menu, F.text.contains("Повторить запрос"))
async def handle_repeat_message(message: Message) -> None:
    if not message.from_user or not (
        user := get_user_by_id_or_none(message.from_user.id)
    ):
        return None
    cities = get_all_city_of_user(user)
    if len(cities) == 0:
        return
    await message.answer(Messages.get_concert_list(cities[0].city_id))

@main_router.message(F.text.contains("Домой"))
async def switch_to_main_menu_if_home(message: Message, state: FSMContext):
    await start_main_menu(message, state)
    await state.set_state(MenuStates.main_menu)


@common_router.message(F.text)
async def handle_unmatched_message(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await send_welcome_message(message)
        return
    await message.answer(
        "Извините, но я не понимаю ваше сообщение. Выберите пункт из меню."
    )


async def send_welcome_message(message: Message):
    await message.answer_photo(
        photo="https://telegra.ph/file/188d44d07bf6497964b69.jpg",
        caption=Messages.get_bot_info(),
    )
