from aiogram import Bot, Dispatcher
from aiogram.types import Message


async def __hello(msg: Message):
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, 'Приветик')


async def __help(msg: Message):
    bot: Bot = msg.bot
    await bot.send_message(msg.from_user.id, 'Мне бы кто помог...')


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__hello, commands='hello')
    dp.register_message_handler(__help, commands='help')
