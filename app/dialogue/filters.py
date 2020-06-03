from typing import Union

import sqlalchemy.orm
from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardButton

from app.db.models import User
from app.db.util import use_db_session, sql_result
from app.trace import trace


@use_db_session
def filter_account_created(message: types.Message, session: sqlalchemy.orm.Session):
    rowcount, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == message.from_user.id))
    if user is None or user.location is None:
        return False
    return True


def filter_button_pressed(button: Union[KeyboardButton, InlineKeyboardButton]):
    if isinstance(button, KeyboardButton):
        def expr(message: types.Message):
            return message.text == button.text
    elif isinstance(button, InlineKeyboardButton):
        def expr(callback_query: types.CallbackQuery):
            return callback_query.data == button.callback_data
    else:
        return None
    return expr
