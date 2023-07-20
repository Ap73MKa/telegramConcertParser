from time import perf_counter

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import MarkupKb, InlineKb
from bot.parsing.controller import create_concerts
from bot.misc import Messages, Config
from bot.database import (
    create_user_city,
    get_user_by_id_or_none,
    delete_outdated_concerts,
    create_user,
    get_all_city_of_user_or_none,
)
from .other import _handle_home_request, _handle_city_check_request, _MenuStates
from ..controls import PathControl


# region Private Functions


# region Handles
async def __handle_response_main(msg: Message, state: FSMContext) -> None:
    if "повторить запрос" in msg.text.lower():
        city_abb = get_all_city_of_user_or_none(
            get_user_by_id_or_none(msg.from_user.id)
        )[0].city_id
        await msg.bot.send_message(
            msg.from_user.id, Messages.get_concert_list(city_abb)
        )
        return

    if "предыдущие запросы" in msg.text.lower():
        cities = [
            city.city.abb
            for city in get_all_city_of_user_or_none(
                get_user_by_id_or_none(msg.from_user.id)
            )
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
        return

    if "поиск концертов по городам" in msg.text.lower():
        user_id = msg.from_user.id
        await state.set_state(_MenuStates.CITY)
        await msg.bot.send_message(
            user_id,
            text=Messages.get_random(),
            reply_markup=MarkupKb.get_city_list(get_user_by_id_or_none(user_id)),
        )
        return

    if "о телеграм боте" in msg.text.lower():
        await state.set_state(_MenuStates.MAIN)
        await msg.bot.send_message(msg.from_user.id, Messages.get_site_info())
        return
    await __welcome(msg, state)


async def __handle_response_city(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    text = msg.text
    user = get_user_by_id_or_none(user_id)
    if text in ("⬅️", "➡️"):
        direction = -1 if text == "⬅️" else 1
        await msg.bot.send_message(
            user_id,
            text=Messages.get_random(),
            reply_markup=MarkupKb.get_city_list(user, direction),
        )
        return
    if await _handle_home_request(msg, state) or await _handle_city_check_request(msg):
        return
    await state.set_state(_MenuStates.MAIN)
    await msg.bot.send_message(
        user_id, text=Messages.get_error_city(), reply_markup=MarkupKb.get_main(user)
    )


async def __handle_response_concert(msg: Message, state: FSMContext) -> None:
    if await _handle_home_request(msg, state) or await _handle_city_check_request(msg):
        return
    await msg.bot.send_message(msg.from_user.id, Messages.get_error_concert())


async def __handle_callback_concert(query: CallbackQuery) -> None:
    create_user_city(get_user_by_id_or_none(query.from_user.id), query.data[5:])
    await query.bot.send_message(
        query.from_user.id, Messages.get_concert_list(query.data[5:])
    )


async def __handle_home_request(msg: Message, state: FSMContext) -> bool:
    if "Домой" in msg.text:
        await state.set_state(_MenuStates.MAIN)
        await msg.bot.send_message(
            msg.from_user.id,
            text=Messages.get_random(),
            reply_markup=MarkupKb.get_main(get_user_by_id_or_none(msg.from_user.id)),
        )
        return True
    return False


# endregion


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
        reply_markup=MarkupKb.get_main(get_user_by_id_or_none(user_id)),
    )


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
