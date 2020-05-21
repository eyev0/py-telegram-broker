from typing import Union

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove


button_upload = InlineKeyboardButton('Залить', callback_data='upload')
button_view = InlineKeyboardButton('Список твоих карт', callback_data='view')
button_delete = InlineKeyboardButton('Удалить', callback_data='delete')

keyboard_menu = InlineKeyboardMarkup()
keyboard_menu.row(button_upload)
keyboard_menu.row(button_view)
keyboard_menu.row(button_delete)
