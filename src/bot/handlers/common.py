from math import ceil

from aiogram.types import InlineKeyboardMarkup
from bot.handlers.messages import Messages
from bot.keyboards.inline import get_nav_city_inline_keyboard

from src.database import City, Concert, Database

MAX_CONCERTS_PER_PAGE = 7


async def get_answer_for_concert_keyboard(
    current_page: int, city: City, db: Database
) -> tuple[str, InlineKeyboardMarkup]:
    concerts = await db.concert.get_many(
        Concert.city_id == city.id,
        order_by=Concert.concert_date,
        limit=10 * MAX_CONCERTS_PER_PAGE,
    )
    max_page = ceil(len(concerts) / MAX_CONCERTS_PER_PAGE)
    page_numb = max(1, min(current_page, max_page))
    start_concert = (page_numb - 1) * MAX_CONCERTS_PER_PAGE
    concerts_on_page = concerts[start_concert : start_concert + MAX_CONCERTS_PER_PAGE]
    text = Messages.get_concert_list(page_numb, max_page, concerts_on_page, city)
    keyboard = get_nav_city_inline_keyboard(city.abb, page_numb)
    return text, keyboard
