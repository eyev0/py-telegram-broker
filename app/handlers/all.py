import sqlalchemy.orm

from app import bot
from app.db import use_db_session, sql_result
from app.db.models import User
from app.handlers.util.decorators import *
from app.handlers.util.keyboards import *
from app.handlers.util.states import States
from app.decorate_log import trace_async, trace


@dp.message_handler(commands=['start'],
                    state='*')
@message_handler_cozy_args
@use_db_session
@trace_async
async def start(user_id, message: types.Message, user_state, session: sqlalchemy.orm.Session):
    rowcount, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == user_id))
    if rowcount == 0:
        trace(User)(uid=user_id,
                    username=message.from_user.username) \
            .insert_me(session)

    await trace_async(user_state.set_state)(States.all()[0])

    await trace_async(message.reply)('Yo',
                                     reply=False,
                                     reply_markup=keyboard_menu)


@dp.callback_query_handler(lambda c: c.data == button_upload.callback_data,
                           state='*')
@dp.message_handler(commands=['upload'],
                    state='*')
@mixed_handler_cozy_args
@use_db_session
@trace_async
async def upload(user_id, message, user_state, is_callback, callback_query, session: sqlalchemy.orm.Session):
    await user_state.set_state(States.all()[1])
    await message.reply('Upload',
                        reply=False)
    if is_callback:
        await bot.answer_callback_query(callback_query.id)
