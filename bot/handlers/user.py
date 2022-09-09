from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.misc import get_concert_list, parse_page
from bot.keyboards.keyboard import get_main_keyboard


async def __parse(msg: Message):
    bot: Bot = msg.bot
    link = 'https://afisha.yandex.ru/vladimir/selections/all-events-concert'
    parse_page(link)
    await bot.send_message(msg.from_user.id, f'Информация обновлена')


async def __concerts(msg: Message):
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, f'Список концертов во Владимире:\n\n'
                                             f'{get_concert_list()}')


async def __start(msg: Message):
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='Здарова братн',
                           reply_markup=get_main_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__parse, content_types=['text'], text='Обновить базу данных ⚙')
    dp.register_message_handler(__concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(__start, commands='start')
