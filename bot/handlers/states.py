from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStates(StatesGroup):
    main_menu = State()
    concert_menu = State()
    city_menu = State()
