from thefuzz.process import extractOne
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.keyboards import MarkupKb
from bot.misc import Messages, simplify_string
from bot.database import get_all_cities_or_none, get_city_by_name_or_none, create_user_city, get_user_by_id_or_none


class _MenuStates(StatesGroup):
    MAIN = State()
    CONCERT = State()
    CITY = State()


# region Handlers

async def _handle_home_request(msg: Message, state: FSMContext) -> bool:
    user_id = msg.from_user.id
    user = get_user_by_id_or_none(user_id)
    if 'Домой' in msg.text:
        await state.set_state(_MenuStates.MAIN)
        await msg.bot.send_message(user_id, text=Messages.get_random(), reply_markup=MarkupKb.get_main(user))
        return True
    return False


async def _handle_city_check_request(msg: Message) -> bool:
    if len(msg.text) <= 2:
        return False
    all_city = [city.simple_name for city in get_all_cities_or_none()]
    close = extractOne(simplify_string(msg.text), all_city)
    if close[1] >= 80:
        city = get_city_by_name_or_none(close[0])
        create_user_city(msg.from_user.id, city.abb)
        await msg.bot.send_message(msg.from_user.id, Messages.get_concert_list(city.abb))
        return True
    return False

# endregion
