from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    SETTINGS_POSTAL_CODE = State()
    INITIAL_REQUEST_CITY = State()
    UPLOAD = State()
    DELETE = State()
    SEARCH = State()
    VIEW = State()
