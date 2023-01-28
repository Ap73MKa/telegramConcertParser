from time import perf_counter
from thefuzz.process import extractOne
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.modules import Messages, simplify_string, Config
from bot.parsing import create_concerts
from bot.database import clean_outdated_concerts, create_user, add_user_city, get_all_city_of_user, get_city_by_name,\
    get_user_by_id, get_all_cities
from .keyboard import get_main_keyboard, get_city_keyboard, get_city_list_keyboard, get_home_keyboard
from .states import MenuStates


async def handle_response_main(msg: Message, state: FSMContext) -> None:
    if 'повторить запрос' in msg.text.lower():
        city_abb = get_all_city_of_user(get_user_by_id(msg.from_user.id))[0].city_id
        await msg.bot.send_message(msg.from_user.id, Messages.get_concert_list(city_abb))
        return

    if 'предыдущие запросы' in msg.text.lower():
        cities = [city.city.abb for city in get_all_city_of_user(get_user_by_id(msg.from_user.id))]
        await state.set_state(MenuStates.concert_menu)
        await msg.bot.send_message(msg.from_user.id, text='Ваш список запросов:', reply_markup=get_home_keyboard())
        await msg.bot.send_message(msg.from_user.id, text=Messages.get_before_list_msg(),
                                   reply_markup=get_city_keyboard(cities))
        return

    if 'поиск концертов по городам' in msg.text.lower():
        await state.set_state(MenuStates.city_menu)
        await msg.bot.send_message(msg.from_user.id, text=Messages.get_random_msg(),
                                   reply_markup=get_city_list_keyboard(get_user_by_id(msg.from_user.id)))
        return

    if 'о телеграм боте' in msg.text.lower():
        await state.set_state(MenuStates.main_menu)
        await msg.bot.send_message(msg.from_user.id, Messages.get_site_info())
        return
    await welcome(msg, state)


async def handle_response_city(msg: Message, state: FSMContext) -> None:
    if msg.text in ('⬅️', '➡️'):
        direction = -1 if msg.text == '⬅️' else 1
        await msg.bot.send_message(msg.from_user.id, text=Messages.get_random_msg(),
                                   reply_markup=get_city_list_keyboard(get_user_by_id(msg.from_user.id), direction))
        return

    if await handle_home_request(msg, state) or await handle_city_check_request(msg):
        return

    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(msg.from_user.id, text=Messages.get_error_city(),
                               reply_markup=get_main_keyboard(get_user_by_id(msg.from_user.id)))


async def handle_response_concert(msg: Message, state: FSMContext) -> None:
    if await handle_home_request(msg, state) or await handle_city_check_request(msg):
        return
    await msg.bot.send_message(msg.from_user.id, Messages.get_error_concert())


async def handle_callback_concert(query: CallbackQuery) -> None:
    add_user_city(get_user_by_id(query.from_user.id), query.data[5:])
    await query.bot.send_message(query.from_user.id, Messages.get_concert_list(query.data[5:]))


async def handle_home_request(msg: Message, state: FSMContext) -> bool:
    if 'Домой' in msg.text:
        await state.set_state(MenuStates.main_menu)
        await msg.bot.send_message(msg.from_user.id, text=Messages.get_random_msg(),
                                   reply_markup=get_main_keyboard(get_user_by_id(msg.from_user.id)))
        return True
    return False


async def handle_city_check_request(msg: Message) -> bool:
    all_city = [city.simple_name for city in get_all_cities()]
    close = extractOne(simplify_string(msg.text), all_city)
    if close[1] >= 80 and len(msg.text) >= 3:
        city = get_city_by_name(close[0])
        add_user_city(get_user_by_id(msg.from_user.id), city.abb)
        await msg.bot.send_message(msg.from_user.id, Messages.get_concert_list(city.abb))
        return True
    return False


async def update(msg: Message) -> None:
    if msg.from_user.id != int(Config.ADMIN_ID):
        return None
    timer = perf_counter()
    clean_outdated_concerts()
    await create_concerts()
    await msg.bot.send_message(msg.from_user.id, Messages.get_update_time(perf_counter() - timer))


async def start(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    create_user(user_id, msg.from_user.full_name)
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(user_id, text=Messages.get_welcome_msg(msg.from_user.full_name),
                               reply_markup=get_main_keyboard(get_user_by_id(user_id)))


async def welcome(msg: Message, state: FSMContext) -> None:
    photo = 'https://sun1-87.userapi.com/impg/wEoV6bpiSXmT3uCKUaB7Cpmj2Nmym5l4hMKnLw/55rB5oNouD4.jpg?size=2000x793&quality=96&sign=7f6fe46af2cbdecd238dfa3d7c435248&type=album'
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_photo(msg.from_user.id, photo=photo, caption=Messages.get_bot_info())


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(update, commands='update', state='*')
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(handle_response_main, state=MenuStates.main_menu)
    dp.register_message_handler(handle_response_city, state=MenuStates.city_menu)
    dp.register_message_handler(handle_response_concert, state=MenuStates.concert_menu)
    dp.register_message_handler(welcome, state='*')
    # endregion

    # region callback handlers
    dp.register_callback_query_handler(handle_callback_concert, lambda c: c.data and c.data.startswith('city-'),
                                       state=MenuStates.concert_menu)
    # endregion
