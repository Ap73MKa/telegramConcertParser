from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.keyboards.keyboard import get_main_keyboard, get_city_keyboard
from bot.database.methods.get import get_concerts_by_city
from bot.misc.config import Config
from bot.misc.reformat import get_cities


async def __start(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text=f'Привет, {msg.from_user.full_name}\n'
                                                  f'Давай узнаем новые концерты',
                           reply_markup=get_main_keyboard())


async def __concerts(msg: Message) -> None:
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, text='Выберите город:', reply_markup=get_city_keyboard())


async def __info(msg: Message):
    bot: Bot = msg.bot
    cities = '\n'.join([f'• {city}' for city in get_cities().values()])
    await bot.send_message(msg.from_user.id, '<b>tgConcerts</b> - это особый телеграм бот, который собирает '
                                             'информацию о всех концертах городов России специально для тебя! '
                                             'Чтобы запустить бота напиши <b>/start</b>\n\n'
                                             f'На данный момент доступны города:\n{cities}')


async def __city_concert(query: CallbackQuery):
    bot: Bot = query.bot
    city_abb = query.data[5:]
    city_name = get_cities()[city_abb]
    concert_list = get_concerts_by_city(city_abb)
    concert_list = '\n'.join([f"{concert.date.strftime('%a, %d %b. %Y')} <i>от {concert.price} ₽</i>\n"
                              f"<b><a href='{concert.url}'>{concert.name}</a></b>\n" for concert in concert_list])
    await bot.send_message(query.from_user.id, f'<a href="https://{city_abb}.{Config.URL}">{city_name.upper()}</a>.'
                                               f' Список концертов\n\n\n{concert_list}')


async def __site(msg: Message):
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, '<b><a href="https://kassir.ru">Kassir</a></b> - сайт, на котором '
                                             'мы и узнаем все информацию об концертах. Если вам неудобен наш бот, то '
                                             'вы всегда можете узнать новую информацию на сайте 🤔')


def register_user_handlers(dp: Dispatcher) -> None:
    # region message handlers
    dp.register_message_handler(__concerts, content_types=['text'], text='Узнать концерты 🔥')
    dp.register_message_handler(__site, content_types=['text'], text='Узнать сайт 💬')
    dp.register_message_handler(__start, commands='start')
    dp.register_message_handler(__info)
    # endregion

    # region callback handlers
    dp.register_callback_query_handler(__city_concert, lambda c: c.data and c.data.startswith('city-'))
    # endregion
