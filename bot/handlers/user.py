from time import perf_counter

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import MarkupKb, InlineKb
from bot.parsing.controller import create_concerts
from bot.misc import Messages, Config
from bot.database import (
    create_user_city,
    get_user_by_id,
    delete_outdated_concerts,
    create_user,
    get_all_city_of_user,
)
from bot.controls import PathControl
from .other import _handle_home_request, _handle_city_check_request, _MenuStates


# region Private Functions


# region Handles


# pylint: disable=W0613
async def __handle_response_repeat(msg: Message, state: FSMContext) -> None:
    city_abb = get_all_city_of_user(get_user_by_id(msg.from_user.id))[0].city_id
    await msg.bot.send_message(msg.from_user.id, Messages.get_concert_list(city_abb))


async def __handle_response_last(msg: Message, state: FSMContext) -> None:
    cities = [
        city.city_id.abb
        for city in get_all_city_of_user(get_user_by_id(msg.from_user.id))
    ]
    await state.set_state(_MenuStates.CONCERT)
    await msg.bot.send_message(
        msg.from_user.id,
        text="Ваш список запросов:",
        reply_markup=MarkupKb.get_home(),
    )
    await msg.bot.send_message(
        msg.from_user.id,
        text=Messages.get_before_list(),
        reply_markup=InlineKb.get_city(cities),
    )


async def __handle_response_search(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    await state.set_state(_MenuStates.CITY)
    await msg.bot.send_message(
        user_id,
        text=msg.text,
        reply_markup=MarkupKb.get_city_list(get_user_by_id(user_id)),
    )


async def __handle_response_about(msg: Message, state: FSMContext) -> None:
    await state.set_state(_MenuStates.MAIN)
    await msg.bot.send_message(msg.from_user.id, Messages.get_site_info())


async def __handle_response_main(msg: Message, state: FSMContext) -> None:
    handlers = {
        "повторить запрос": __handle_response_repeat,
        "предыдущие запросы": __handle_response_last,
        "поиск концертов по городам": __handle_response_search,
        "о телеграм боте": __handle_response_about,
    }
    for key, handler in handlers.items():
        if key in msg.text.lower():
            await handler(msg, state)
            return
    await __welcome(msg, state)


async def _handle_pagination_buttons(msg: Message) -> bool:
    user_id = msg.from_user.id
    message_text = msg.text
    user = get_user_by_id(user_id)
    if message_text in ("⬅️", "➡️"):
        direction = -1 if message_text == "⬅️" else 1
        await msg.bot.send_message(
            user_id,
            text=msg.text,
            reply_markup=MarkupKb.get_city_list(user, direction),
        )
        return True
    return False


async def __handle_response_city(msg: Message, state: FSMContext) -> None:
    if (
        await _handle_pagination_buttons(msg)
        or await _handle_home_request(msg, state)
        or await _handle_city_check_request(msg)
    ):
        return
    user_id = msg.from_user.id
    user = get_user_by_id(user_id)
    await state.set_state(_MenuStates.MAIN)
    await msg.bot.send_message(
        user_id, text=Messages.get_error_city(), reply_markup=MarkupKb.get_main(user)
    )


async def __handle_response_concert(msg: Message, state: FSMContext) -> None:
    if await _handle_home_request(msg, state) or await _handle_city_check_request(msg):
        return
    await msg.bot.send_message(msg.from_user.id, Messages.get_error_concert())


async def __handle_callback_concert(query: CallbackQuery) -> None:
    create_user_city(get_user_by_id(query.from_user.id), query.data[5:])
    await query.bot.send_message(
        query.from_user.id, Messages.get_concert_list(query.data[5:])
    )


async def __handle_home_request(msg: Message, state: FSMContext) -> bool:
    if "Домой" in msg.text:
        await state.set_state(_MenuStates.MAIN)
        await msg.bot.send_message(
            msg.from_user.id,
            text=msg.text,
            reply_markup=MarkupKb.get_main(get_user_by_id(msg.from_user.id)),
        )
        return True
    return False


async def __update(msg: Message) -> None:
    user_id = msg.from_user.id
    if user_id != int(Config.ADMIN_ID):
        return None
    timer = perf_counter()
    delete_outdated_concerts()
    await create_concerts()
    await msg.bot.send_message(
        user_id, Messages.get_update_time(perf_counter() - timer)
    )


async def __welcome(msg: Message, state: FSMContext) -> None:
    with open(PathControl.get("assets/banner.jpg"), "rb") as photo:
        await state.set_state(_MenuStates.MAIN)
        await msg.bot.send_photo(
            msg.from_user.id, photo=photo, caption=Messages.get_bot_info()
        )


async def __start(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    create_user(user_id, msg.from_user.full_name)
    await state.set_state(_MenuStates.MAIN)
    await msg.bot.send_message(
        user_id,
        text=Messages.get_welcome(msg.from_user.full_name),
        reply_markup=MarkupKb.get_main(get_user_by_id(user_id)),
    )


# endregion


# endregion

# region Public Functions


def register_user_handlers(dp: Dispatcher) -> None:
    # region Message handlers

    dp.register_message_handler(__update, commands="update", state="*")
    dp.register_message_handler(__start, commands="start", state="*")
    dp.register_message_handler(__handle_response_main, state=_MenuStates.MAIN)
    dp.register_message_handler(__handle_response_city, state=_MenuStates.CITY)
    dp.register_message_handler(__handle_response_concert, state=_MenuStates.CONCERT)
    dp.register_message_handler(__welcome, state="*")

    # endregion

    # region Callback handlers

    dp.register_callback_query_handler(
        __handle_callback_concert,
        lambda c: c.data and c.data.startswith("city-"),
        state=_MenuStates.CONCERT,
    )

    # endregion


# endregion
