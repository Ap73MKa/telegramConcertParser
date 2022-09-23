from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.misc import update_database
from bot.keyboards.keyboard import get_main_keyboard, get_city_keyboard
from bot.database.methods.get import get_all_concerts


async def __update_db(msg: Message) -> None:
    bot: Bot = msg.bot
    update_database()
    await bot.send_message(msg.from_user.id, 'Информация обновлена')


async def __concerts(msg: Message) -> None:
    bot: Bot = msg.bot
    concert_list = reversed(get_all_concerts())
    concert_list = '\n'.join([f'{concert.date} <b>{concert.name}</b> <i>от {concert.price}₽</i>'
                              for concert in concert_list])
    await bot.send_message(msg.from_user.id, f'Список концертов во Владимире:\n\n'
                                             f'{concert_list}')


async def __start(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='Начнем парсинг',
                           reply_markup=get_main_keyboard())


async def __test(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='ffff', reply_markup=get_city_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__update_db, content_types=['text'], text='Обновить базу данных ⚙')
    dp.register_message_handler(__concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(__start, commands='start')
    dp.register_message_handler(__test, commands='test')
