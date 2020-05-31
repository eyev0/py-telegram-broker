import io

import sqlalchemy.orm

from app.db import use_db_session, sql_result
from app.db.models import User
from app.trace import trace_async, trace
from app.handlers.util.parse_args import *
from app.handlers.util.keyboards import *
from app.handlers.util.states import States, resolve_state, CreateAccountStates


@dp.message_handler(commands=['start'],
                    state='*')
@resolve_state
@parse_args(mode='message')
@use_db_session
@trace_async
async def start(user_id,
                user_state,
                message: types.Message,
                session: sqlalchemy.orm.Session):
    next_state = States.STATE_0_INITIAL
    rowcount, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == user_id))
    if rowcount == 0:
        trace(User)(uid=user_id,
                    username=message.from_user.username) \
            .insert_me(session)
        await trace_async(message.reply)('Yo, давай знакомиться. '
                                         'В каком городе ты живешь?',
                                         reply=False)
        next_state = CreateAccountStates.CREATE_ACC_STATE_0_CITY

    return next_state


@dp.message_handler(commands=['upload'],
                    state='*')
@resolve_state
@parse_args(mode='message')
@use_db_session
@trace_async
async def upload(user_id,
                 user_state,
                 message: types.Message,
                 session: sqlalchemy.orm.Session):
    next_state = States.STATE_0_INITIAL
    if not message.document:
        await message.reply('Yo, скинь мне файл вместе с этой командой, чтобы загрузить карты.\n',
                            reply=True)
    dest_io = io.StringIO()
    await message.document.download(dest_io)
    text_wrapper = io.TextIOWrapper(dest_io)
    text_wrapper.read()
    pass


@dp.message_handler(commands=['mycards'],
                    state='*')
@resolve_state
@parse_args(mode='message')
@use_db_session
@trace_async
async def mycards(user_id,
                  user_state,
                  message: types.Message,
                  session: sqlalchemy.orm.Session):
    await message.reply('Show me my cards',
                        reply=False)
