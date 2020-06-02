import sqlalchemy.orm
from aiogram import types

from app import dp, config
from app.db import use_db_session, sql_result
from app.db.models import User
from app.dialogue import checks
from app.dialogue.checks import is_from_su, is_from_admin, filter_account_created
from app.dialogue.messages import MESSAGES
from app.dialogue.util.parse_args import parse_args
from app.dialogue.util.states import States, resolve_state, CreateAccountStates
from app.trace import trace_async, trace


@dp.message_handler(is_from_su,
                    commands=['admin'],
                    state='*')
@parse_args(mode='message')
@trace_async
async def admin(user_id,
                user_state,
                message: types.Message):
    if not is_from_admin(message):
        config.app.admin.append(user_id)
        await message.reply(MESSAGES['admin_enable'], reply=False)
    else:
        config.app.admin.remove(user_id)
        await message.reply(MESSAGES['admin_disable'], reply=False)


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


@dp.message_handler(filter_account_created,
                    commands=['upload'],
                    state='*')
@resolve_state
@parse_args(mode='message')
@use_db_session
@trace_async
async def upload_command(user_id,
                         user_state,
                         message: types.Message,
                         session: sqlalchemy.orm.Session):
    upload_rowcount = 0

    _, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == user_id))

    passed, next_state, message_text = checks.upload(user, upload_rowcount, session)
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
