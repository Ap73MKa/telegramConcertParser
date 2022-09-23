from aiogram import Bot, Dispatcher
from bot.misc import update_database
from aiogram.types import Message, CallbackQuery
from bot.keyboards.keyboard import get_main_keyboard, get_city_keyboard
from bot.database.methods.get import get_concerts_by_city
from bot.misc.reformat import get_cities


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
    concert_list = reversed(get_concerts_by_city(query.data[5:]))
    concert_list = '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                              for concert in concert_list])
    city_name = get_cities()[query.data[5:]]
    await bot.send_message(query.from_user.id, f'{city_name}. Список концертов\n\n{concert_list}')


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(__update_db, content_types=['text'], text='Обновить базу данных ⚙')
    dp.register_message_handler(__concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(__start, commands='start')

    # region callback handlers
    dp.register_callback_query_handler(__city_concert, lambda c: c.data and c.data.startswith('city-'))
