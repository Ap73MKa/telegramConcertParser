from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    main_menu = State()
    concert_menu = State()
    city_menu = State()
