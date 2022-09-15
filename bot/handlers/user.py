from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.misc import get_concert_list, update_database, EnvKeys
from bot.keyboards.keyboard import get_main_keyboard


async def __update_db(msg: Message) -> None:
    bot: Bot = msg.bot
    update_database(EnvKeys.LINK)
    await bot.send_message(msg.from_user.id, f'Информация обновлена')


async def __concerts(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, f'Список концертов во Владимире:\n\n'
                                             f'{get_concert_list()}')


async def __start(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='Начнем парсинг',
                           reply_markup=get_main_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__update_db, content_types=['text'], text='Обновить базу данных ⚙')
    dp.register_message_handler(__concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(__start, commands='start')
