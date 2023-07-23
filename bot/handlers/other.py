# from thefuzz.process import extractOne
# from aiogram.types import Message
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
#
# from bot.keyboards import MarkupKb
# from bot.misc import Messages, simplify_string
# from bot.database import (
#     get_all_cities,
#     get_city_by_name_or_none,
#     create_user_city,
#     get_user_by_id,
# )
#
#
# class _MenuStates(StatesGroup):
#     MAIN = State()
#     CONCERT = State()
#     CITY = State()
#
#
# # region Handlers
#
#
# async def _handle_home_request(msg: Message, state: FSMContext) -> bool:
#     if not (user := get_user_by_id(msg.from_user.id)):
#         return False
#     if "Домой" in msg.text:
#         await state.set_state(_MenuStates.MAIN)
#         await msg.bot.send_message(
#             msg.from_user.id,
#             text=msg.text,
#             reply_markup=MarkupKb.get_main(user),
#         )
#         return True
#     return False
#
#
# async def _handle_city_check_request(msg: Message) -> bool:
#     if len(msg.text) <= 2:
#         return False
#     close = extractOne(
#         simplify_string(msg.text),
#         [city.simple_name for city in get_all_cities()],
#     )
#     if close[1] >= 80:
#         city_abb = get_city_by_name_or_none(close[0]).abb
#         create_user_city(msg.from_user.id, city_abb)
#         await msg.bot.send_message(
#             msg.from_user.id, Messages.get_concert_list(city_abb)
#         )
#         return True
#     return False
#
#
# # endregion
