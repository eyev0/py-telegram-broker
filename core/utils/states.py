from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    INITIAL_REQUEST_CITY = State()
    UPLOAD = State()
    DELETE = State()
    SEARCH = State()
    VIEW = State()
