import sqlalchemy.orm

from app.db import use_db_session, sql_result
from app.db.models import User
from app.handlers.messages import MESSAGES
from app.handlers.util.parse_args import *
from app.handlers.util.states import States, resolve_state, CreateAccountStates
from app.trace import trace_async, trace


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
        await trace_async(message.reply)(MESSAGES['greetings'],
                                         reply=False)
        next_state = CreateAccountStates.CREATE_ACC_STATE_0_CITY

    return next_state


@dp.message_handler(commands=['upload'],
                    state='*')
@resolve_state
@parse_args(mode='message')
@use_db_session
@trace_async
async def upload_command(user_id,
                         user_state,
                         message: types.Message,
                         session: sqlalchemy.orm.Session):
    _, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == user_id))

    passed, next_state, message_text = user.check_upload_restrictions(session)
    await message.reply(message_text,
                        reply=True)
    return next_state


@dp.message_handler(state=States.STATE_1_UPLOAD)
@resolve_state
@parse_args(mode='message')
@use_db_session
@trace_async
async def upload_action(user_id,
                        user_state,
                        message: types.Message,
                        session: sqlalchemy.orm.Session):
    next_state = States.STATE_0_INITIAL
    await message.reply(MESSAGES['upload_complete'],
                        reply=True)


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
