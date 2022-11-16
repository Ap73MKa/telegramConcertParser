from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.modules import Messages, get_cities
from bot.parsing import create_concerts
from bot.database import clean_outdated_concerts, create_user, get_user_by_id
from bot.keyboards import get_main_keyboard, get_city_keyboard
from .states import MenuStates
from bot.database.city_list import add_user_city


async def start(msg: Message, state: FSMContext) -> None:
    create_user(msg.from_user.id)
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(msg.from_user.id, text=Messages.get_welcome_msg(msg.from_user.full_name),
                               reply_markup=get_main_keyboard())


async def concerts(msg: Message, state: FSMContext) -> None:
    user = get_user_by_id(msg.from_user.id)
    cities = user.cities.split(sep='||')
    await msg.bot.send_message(msg.from_user.id, text=Messages.get_before_list_msg(),
                               reply_markup=get_city_keyboard(cities))
    await state.set_state(MenuStates.choose_city)


async def init_city_by_msg(msg: Message, state: FSMContext) -> None:
    text = msg.text.lower().strip()
    user_id = msg.from_user.id

    city_abb = None
    for key, value in get_cities().items():
        if value.lower() == text:
            city_abb = key

    if city_abb:
        add_user_city(user_id, city_abb)
        await state.set_state(MenuStates.main_menu)
        await msg.bot.send_message(user_id, Messages.get_concert_list(city_abb))
    else:
        await msg.bot.send_message(user_id, 'Ошибка ввода, повторите попытку')


async def info(msg: Message, state: FSMContext) -> None:
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(msg.from_user.id, Messages.get_bot_info())


async def city_concert(query: CallbackQuery, state: FSMContext) -> None:
    add_user_city(query.from_user.id, query.data[5:])
    await state.set_state(MenuStates.main_menu)
    await query.bot.send_message(query.from_user.id, Messages.get_concert_list(query.data[5:]))


async def site(msg: Message, state: FSMContext) -> None:
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(msg.from_user.id, Messages.get_site_info())


async def check(msg: Message) -> None:
    clean_outdated_concerts()
    await create_concerts()
    await msg.bot.send_message(msg.from_user.id, 'Checked')


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(concerts, content_types=['text'], text='Узнать концерты 🔥', state=MenuStates.main_menu)
    dp.register_message_handler(site, content_types=['text'], text='Узнать сайт 💬', state=MenuStates.main_menu)
    dp.register_message_handler(check, commands='check', state=MenuStates.main_menu)
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(init_city_by_msg, state=MenuStates.choose_city)
    dp.register_message_handler(info, state='*')
    # endregion

    # region callback handlers
    dp.register_callback_query_handler(city_concert, lambda c: c.data and c.data.startswith('city-'),
                                       state=MenuStates.choose_city)
    # endregion
