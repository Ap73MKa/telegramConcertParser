from time import perf_counter
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile

from bot.modules import Messages, simplify_string, Config, PathManager
from bot.parsing import create_concerts
from bot.database import clean_outdated_concerts, create_user, add_user_city, get_all_city_of_user, get_city_by_name,\
    get_user_by_id
from bot.keyboards import get_main_keyboard, get_city_keyboard, get_city_list_keyboard, get_home_keyboard

from .states import MenuStates


async def concert_menu(msg: Message, state: FSMContext) -> None:
    cities = [city.city.abb for city in get_all_city_of_user(msg.from_user.id)]
    await state.set_state(MenuStates.concert_menu)
    await msg.bot.send_message(msg.from_user.id, text='Ваш список запросов:',
                               reply_markup=get_home_keyboard())
    await msg.bot.send_message(msg.from_user.id, text=Messages.get_before_list_msg(),
                               reply_markup=get_city_keyboard(cities))


async def city_menu(msg: Message, state: FSMContext) -> None:
    user = get_user_by_id(msg.from_user.id)
    await state.set_state(MenuStates.city_menu)
    await msg.bot.send_message(msg.from_user.id, text='Выберите город',
                               reply_markup=get_city_list_keyboard(user, user.city_page))


async def about(msg: Message, state: FSMContext) -> None:
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(msg.from_user.id, Messages.get_site_info())


async def handle_response_city(msg: Message, state: FSMContext) -> None:
    user = get_user_by_id(msg.from_user.id)
    if msg.text == '⬅️':
        await msg.bot.send_message(msg.from_user.id, text='Выберите город',
                                   reply_markup=get_city_list_keyboard(user, user.city_page - 1))
        return

    if msg.text == '➡️':
        await msg.bot.send_message(msg.from_user.id, text='Выберите город',
                                   reply_markup=get_city_list_keyboard(user, user.city_page + 1))
        return

    if 'Домой' in msg.text:
        await state.set_state(MenuStates.main_menu)
        await msg.bot.send_message(msg.from_user.id, text=Messages.get_random_msg(), reply_markup=get_main_keyboard())
        return

    city = get_city_by_name(simplify_string(msg.text))
    if city:
        add_user_city(msg.from_user.id, city.abb)
        await msg.bot.send_message(msg.from_user.id, Messages.get_concert_list(city.abb))
        return

    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(msg.from_user.id, text='Ошибка ввода, возвращаю в главное меню',
                               reply_markup=get_main_keyboard())


async def handle_response_concert(msg: Message, state: FSMContext) -> None:
    if 'Домой' in msg.text:
        await state.set_state(MenuStates.main_menu)
        await msg.bot.send_message(msg.from_user.id, text=Messages.get_random_msg(), reply_markup=get_main_keyboard())
        return

    city = get_city_by_name(simplify_string(msg.text))
    if city:
        add_user_city(msg.from_user.id, city.abb)
        await msg.bot.send_message(msg.from_user.id, Messages.get_concert_list(city.abb))
    else:
        await msg.bot.send_message(msg.from_user.id, 'Пожалуйста, введите название города или выберите город из списка')


async def handle_callback_concert(query: CallbackQuery, state: FSMContext) -> None:
    add_user_city(query.from_user.id, query.data[5:])
    await query.bot.send_message(query.from_user.id, Messages.get_concert_list(query.data[5:]))


async def update(msg: Message) -> None:
    if msg.from_user.id != int(Config.ADMIN_ID):
        return None
    timer = perf_counter()
    clean_outdated_concerts()
    await create_concerts()
    elapsed = perf_counter() - timer
    await msg.bot.send_message(msg.from_user.id, f'База данных обновлена.\nВыполнено за: {elapsed:.1f} сек.')


async def start(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    create_user(user_id, msg.from_user.full_name)
    add_user_city(user_id, 'msk')
    add_user_city(user_id, 'spb')
    await state.set_state(MenuStates.main_menu)
    await msg.bot.send_message(user_id, text=Messages.get_welcome_msg(msg.from_user.full_name),
                               reply_markup=get_main_keyboard())


async def welcome(msg: Message, state: FSMContext) -> None:
    info_img = InputFile(PathManager.get('assets/info.png'))
    await msg.bot.send_photo(msg.from_user.id, photo=info_img, caption=Messages.get_bot_info())
    await state.set_state(MenuStates.main_menu)


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(concert_menu, content_types=['text'], text='Предыдущие запросы 🔥',
                                state=MenuStates.main_menu)
    dp.register_message_handler(city_menu, content_types=['text'], text='Поиск концертов по городам 💥',
                                state=MenuStates.main_menu)
    dp.register_message_handler(about, content_types=['text'], text='О телеграм боте 💬',
                                state=MenuStates.main_menu)
    dp.register_message_handler(handle_response_city, state=MenuStates.city_menu)
    dp.register_message_handler(handle_response_concert, state=MenuStates.concert_menu)
    dp.register_message_handler(update, commands='update', state=MenuStates.main_menu)
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(welcome, state='*')
    # endregion

    # region callback handlers
    dp.register_callback_query_handler(handle_callback_concert, lambda c: c.data and c.data.startswith('city-'),
                                       state=MenuStates.concert_menu)
    # endregion
