from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from bot.keyboards import get_main_keyboard, get_city_keyboard
from bot.misc import Texts
# from bot.parsing.schedule import update_database


async def start(msg: Message) -> None:
    await msg.bot.send_message(msg.from_user.id, text=Texts.get_welcome_msg(msg.from_user.full_name),
                               reply_markup=get_main_keyboard())


async def concerts(msg: Message) -> None:
    await msg.bot.send_message(msg.from_user.id, text='Выберите город:', reply_markup=get_city_keyboard())


async def info(msg: Message) -> None:
    await msg.bot.send_message(msg.from_user.id, Texts.get_bot_info())


async def city_concert(query: CallbackQuery) -> None:
    await query.bot.send_message(query.from_user.id, Texts.get_concert_list(query.data[5:]))


async def site(msg: Message) -> None:
    await msg.bot.send_message(msg.from_user.id, Texts.get_site_info())


# async def check(msg: Message) -> None:
#     await update_database()
#     await msg.bot.send_message(msg.from_user.id, 'Checked')


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(site, content_types=['text'], text='Узнать сайт 💬')
    dp.register_message_handler(start, commands='start')
    # dp.register_message_handler(check, commands='check')
    dp.register_message_handler(info)
    # endregion

    # region callback handlers
    dp.register_callback_query_handler(city_concert, lambda c: c.data and c.data.startswith('city-'))
    # endregion
