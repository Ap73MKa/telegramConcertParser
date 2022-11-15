from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStates(StatesGroup):
    main_menu = State()
    choose_city = State()
