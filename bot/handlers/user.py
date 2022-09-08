from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.misc import get_concert_list


async def __parse(msg: Message):
    bot: Bot = msg.bot
    concert_list = get_concert_list()
    await bot.send_message(msg.from_user.id, f'Список концертов:\n{concert_list}')


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__parse, commands='parse')
