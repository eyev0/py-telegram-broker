from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils.helper import Item, Helper, HelperMode


class StateItem(Item):
    pass


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0_REQUEST_CITY = StateItem()
    STATE_1_MAIN = StateItem()
    STATE_2_UPLOAD = StateItem()
    STATE_3_DELETE = StateItem()
    STATE_4_SEARCH = StateItem()
    STATE_5_VIEW = StateItem()


keyboard_remove = ReplyKeyboardRemove()

button_geo = KeyboardButton('Отправить свою геолокацию', request_location=True)
keyboard_geo = ReplyKeyboardMarkup().row(button_geo)

button_upload = InlineKeyboardButton('Залить', callback_data='upload')
button_view = InlineKeyboardButton('Мои карты', callback_data='view')
button_delete = InlineKeyboardButton('Удалить карты', callback_data='delete')

keyboard_menu = InlineKeyboardMarkup()
keyboard_menu.row(button_upload)
keyboard_menu.row(button_view)
keyboard_menu.row(button_delete)
