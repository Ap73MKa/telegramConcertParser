from time import perf_counter

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile

from bot.parsing import create_concerts
from bot.keyboards import InlineKb, MarkupKb
from bot.misc import Messages, Config
from bot.controls import PathControl
from bot.database import delete_outdated_concerts, create_user, create_user_city, \
    get_all_city_of_user_or_none, get_user_by_id_or_none

from .other import _MenuStates, _handle_home_request, _handle_city_check_request


# region Private Functions
async def __city_menu(msg: Message, state: FSMContext) -> None:
    await state.set_state(_MenuStates.CITY)
    await msg.bot.send_message(msg.from_user.id, text=Messages.get_random(),
                               reply_markup=MarkupKb.get_city_list(get_user_by_id_or_none(msg.from_user.id), 0))


async def __concert_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    cities = [city.city.abb for city in get_all_city_of_user_or_none(user_id)]
    await state.set_state(_MenuStates.CONCERT)
    await msg.bot.send_message(msg.from_user.id, text='Ваш список запросов:', reply_markup=MarkupKb.get_home())
    await msg.bot.send_message(
        user_id, text=Messages.get_before_list(), reply_markup=InlineKb.get_city(cities)
    )


async def __handle_response_city(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    text = msg.text
    if text in ('⬅️', '➡️'):
        dir = -1 if text == '⬅️' else 1
        await msg.bot.send_message(user_id, text=Messages.get_random(),
                                   reply_markup=MarkupKb.get_city_list(get_user_by_id_or_none(user_id), dir))
        return
    if await _handle_home_request(msg, state) or await _handle_city_check_request(msg):
        return
    await state.set_state(_MenuStates.Main)
    await msg.bot.send_message(user_id, text=Messages.get_error_city(), reply_markup=MarkupKb.get_main())


async def __handle_response_concert(msg: Message, state: FSMContext) -> None:
    if await _handle_home_request(msg, state) or await _handle_city_check_request(msg):
        return
    await msg.bot.send_message(msg.from_user.id, Messages.get_error_concert())


async def __handle_callback_concert(query: CallbackQuery, state: FSMContext) -> None:
    create_user_city(query.from_user.id, query.data[5:])
    await query.bot.send_message(query.from_user.id, Messages.get_concert_list(query.data[5:]))


async def __update(msg: Message) -> None:
    user_id = msg.from_user.id
    if user_id != int(Config.ADMIN_ID):
        return None
    timer = perf_counter()
    delete_outdated_concerts()
    await create_concerts()
    await msg.bot.send_message(user_id, Messages.get_update_time(perf_counter() - timer))


async def __about(msg: Message, state: FSMContext) -> None:
    await state.set_state(_MenuStates.Main)
    await msg.bot.send_message(msg.from_user.id, Messages.get_site_info())


async def __welcome(msg: Message, state: FSMContext) -> None:
    info_img = InputFile(PathControl.get('assets/info.png'))
    await msg.bot.send_photo(msg.from_user.id, photo=info_img, caption=Messages.get_bot_info())
    await state.set_state(_MenuStates.Main)


async def __start(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    create_user(user_id, msg.from_user.full_name)
    create_user_city(user_id, 'msk')
    create_user_city(user_id, 'spb')
    await state.set_state(_MenuStates.Main)
    await msg.bot.send_message(user_id, text=Messages.get_welcome(msg.from_user.full_name),
                               reply_markup=MarkupKb.get_main())


# endregion


# region Public Functions
def register_user_handlers(dp: Dispatcher) -> None:
    # region Message handlers

    dp.register_message_handler(
        __concert_menu, content_types=['text'], text='Предыдущие запросы 🔥', state=_MenuStates.Main
    )
    dp.register_message_handler(
        __city_menu, content_types=['text'], text='Поиск концертов по городам 💥', state=_MenuStates.Main
    )
    dp.register_message_handler(
        __about, content_types=['text'], text='О телеграм боте 💬', state=_MenuStates.Main
    )
    dp.register_message_handler(__handle_response_city, state=_MenuStates.CITY)
    dp.register_message_handler(__handle_response_concert, state=_MenuStates.CONCERT)
    dp.register_message_handler(__update, commands='update', state=_MenuStates.Main)
    dp.register_message_handler(__start, commands='start', state='*')
    dp.register_message_handler(__welcome, state='*')

    # endregion

    # region Callback handlers

    dp.register_callback_query_handler(
        __handle_callback_concert, lambda c: c.data and c.data.startswith('city-'), state=_MenuStates.CONCERT
    )

    # endregion

# endregion
