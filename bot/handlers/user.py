from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.keyboards.keyboard import get_main_keyboard, get_city_keyboard
from bot.database.methods.get import get_concerts_by_city
from bot.misc import Config, update_database, get_cities


async def __update_db(msg: Message) -> None:
    bot: Bot = msg.bot
    await update_database()
    await bot.send_message(msg.from_user.id, 'Информация обновлена')


async def __start(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='Начнем парсинг',
                           reply_markup=get_main_keyboard())


async def __concerts(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='Выберите город:', reply_markup=get_city_keyboard())


async def __city_concert(query: CallbackQuery):
    bot: Bot = query.bot
    city_abb = query.data[5:]
    city_name = get_cities()[city_abb]
    concert_list = get_concerts_by_city(city_abb)
    concert_list = '\n'.join([f"{concert.date.strftime('%d %b, %a %Y')} <i>от {concert.price} ₽</i>\n"
                              f"<b><a href='{concert.url}'>{concert.name}</a></b>\n" for concert in concert_list])
    await bot.send_message(query.from_user.id, f'<a href="https://{city_abb}.{Config.URL}">{city_name.upper()}</a>.'
                                               f' Список концертов\n\n\n{concert_list}')


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(__update_db, content_types=['text'], text='Обновить базу данных ⚙')
    dp.register_message_handler(__concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(__start, commands='start')
    # endregion

    # region callback handlers
    dp.register_callback_query_handler(__city_concert, lambda c: c.data and c.data.startswith('city-'))
    # endregion
