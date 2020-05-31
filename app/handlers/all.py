import sqlalchemy.orm

from app.db import use_db_session, sql_result
from app.db.models import User
from app.log import trace_async, trace
from app.handlers.util.parse_args import *
from app.handlers.util.keyboards import *
from app.handlers.util.states import States


@dp.message_handler(commands=['start'],
                    state='*')
@message_handler_parse_args
@use_db_session
@trace_async
async def start(user_id, user_state, message: types.Message, session: sqlalchemy.orm.Session):
    rowcount, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == user_id))
    if rowcount == 0:
        # create user
        trace(User)(uid=user_id,
                    username=message.from_user.username)\
            .insert_me(session)

    await trace_async(message.reply)('Yo',
                                     reply=False,
                                     reply_markup=keyboard_menu)
    return States.STATE_1_UPLOAD


@dp.callback_query_handler(lambda c: c.data == button_upload.callback_data,
                           state='*')
@dp.message_handler(commands=['upload'],
                    state='*')
@mixed_handler_parse_args
@use_db_session
@trace_async
async def upload(user_id, user_state, message, callback_query, session: sqlalchemy.orm.Session):
    await message.reply('Upload',
                        reply=False)
