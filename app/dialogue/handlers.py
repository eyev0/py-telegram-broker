import re
from typing import Union, List

import sqlalchemy.orm
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from app import dp, config
from app.db.models import User, Item
from app.dialogue import StateItem, States
from app.dialogue import keyboard_remove
from app.dialogue.filters import filter_su, filter_admin, filter_user_inactive
from app.messages import MESSAGES
from app.middlewares import trace, add_middlewares, sql_result


# inactive
@dp.message_handler(filter_user_inactive,
                    state='*')
@add_middlewares(use_resolve_state=True,
                 use_trace=True)
async def inactive(uid,
                   context,
                   message: types.Message) -> Union[StateItem, None]:
    await message.reply(MESSAGES['user_inactive'], reply=False)
    return States.STATE_1_MAIN


# /admin
@dp.message_handler(filter_su,
                    commands=['admin'],
                    state='*')
@add_middlewares(use_trace=True)
async def admin(uid,
                context,
                message: types.Message):
    if not filter_admin(message):
        config.app.admin.append(uid)
        await message.reply(MESSAGES['admin_enable'], reply=False)
    else:
        config.app.admin.remove(uid)
        await message.reply(MESSAGES['admin_disable'], reply=False)


# /clear
@dp.message_handler(filter_su,
                    commands=['clear'],
                    state='*')
@add_middlewares(use_resolve_state=True,
                 use_trace=True)
async def clear_state(uid,
                      context,
                      message: types.Message) -> Union[StateItem, None]:
    return States.STATE_1_MAIN


# /start
@dp.message_handler(commands=['start'],
                    state='*')
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def start(uid,
                context,
                message: types.Message,
                session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    rowcount, user, _ = sql_result(session.query(User)
                                   .filter(User.uid == uid))
    if rowcount == 0:
        trace(User)(uid=uid,
                    username=message.from_user.username) \
            .insert_me(session)
        reply_text = MESSAGES['greetings']
        next_state = States.STATE_0_REQUEST_CITY
    else:
        reply_text = MESSAGES['yo']
        next_state = States.STATE_1_MAIN
    await message.reply(reply_text, reply=False)

    return next_state


# get geo
@dp.message_handler(state=States.STATE_0_REQUEST_CITY,
                    content_types=ContentTypes.TEXT)
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def request_city(uid,
                       context,
                       message: types.Message,
                       session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    rowcount, user, _ = sql_result(session.query(User)
                                   .filter(User.uid == uid),
                                   raise_on_empty_result=True)
    user.location = message.text
    await message.reply(MESSAGES['sign_up_complete'],
                        reply=False,
                        reply_markup=keyboard_remove)
    next_state = States.STATE_1_MAIN
    return next_state


# /cancel
@dp.message_handler(commands=['cancel'],
                    state=[States.STATE_2_UPLOAD, States.STATE_3_DELETE, States.STATE_4_SEARCH])
@add_middlewares(use_resolve_state=True,
                 use_trace=True)
async def cancel(uid,
                 context,
                 message: types.Message) -> Union[StateItem, None]:
    await message.reply(MESSAGES['cancel'])
    return States.STATE_1_MAIN


# /upload
@dp.message_handler(commands=['upload'],
                    state=States.STATE_1_MAIN)
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def upload_command(uid,
                         context,
                         message: types.Message,
                         session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    _, user, _ = sql_result(session.query(User)
                            .filter(User.uid == uid),
                            raise_on_empty_result=True)
    await message.reply(MESSAGES['upload'])
    return States.STATE_2_UPLOAD


def parse_upload(raw_text: str,
                 user_id: int,
                 row_delimiter='\n',
                 column_delimiter=',',
                 trim_carriage_return=True) -> Union[List[Item], None]:
    result = []
    if trim_carriage_return:
        raw_text = raw_text.replace('\r', '')
    rows = raw_text.split(row_delimiter)
    for a in [row.split(column_delimiter) for row in rows]:
        if len(a) != 2:
            result = None
            break
        else:
            result.append(Item(user_id, name=a[0], price=a[1]))
    return result


# process /upload
@dp.message_handler(state=States.STATE_2_UPLOAD)
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def upload_parse_rows(uid,
                            context,
                            message: types.Message,
                            session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    _, user, _ = sql_result(session.query(User)
                            .filter(User.uid == uid),
                            raise_on_empty_result=True)
    items_list = parse_upload(message.text, user.id)
    if items_list is None:
        await message.reply(MESSAGES['upload_parse_failed'])
        return States.STATE_2_UPLOAD
    rowcount, _, _ = sql_result(session.query(Item)
                                .filter(Item.owner_id == user.id)
                                .filter(Item.status < 9))
    if len(items_list) + rowcount > user.limit:
        await message.reply(MESSAGES['upload_limit_exceeded'].format(user.limit, message.text))
        return States.STATE_1_MAIN
    for item in items_list:
        item.insert_me(session)
    await message.reply(MESSAGES['upload_complete'])
    return States.STATE_1_MAIN


def parse_delete(raw_text: str,
                 uid: int,
                 session: sqlalchemy.orm.Session) -> Union[List, None]:
    if raw_text == 'all':
        _, user, _ = sql_result(session.query(User)
                                .filter(User.uid == uid))
        del_records = user.owner_items
    elif re.findall('[^0-9, ]', raw_text):
        return None
    else:
        ls = [x.strip() for x in raw_text.split(',')]
        _, _, del_records = sql_result(session.query(Item)
                                       .join(User)
                                       .filter(User.uid == uid)
                                       .filter(Item.id.in_(ls)))
    return del_records or []


# /delete
@dp.message_handler(commands=['delete'],
                    state=States.STATE_1_MAIN)
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def delete_command(uid,
                         context: FSMContext,
                         message: types.Message,
                         session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    # save del_ids and request confirmation
    args: str = message.get_args()
    if len(args) == 0:
        await message.reply(MESSAGES['delete_help'])
        return States.STATE_1_MAIN
    items_list = parse_delete(args, uid, session)
    if items_list is None:
        await message.reply(MESSAGES['delete_format_error'])
        return States.STATE_1_MAIN
    if not items_list:
        await message.reply(MESSAGES['delete_no_records'])
        return States.STATE_1_MAIN
    s = '\n'.join([f'{item.row_repr()}' for item in items_list])
    await message.reply(MESSAGES['delete_records_confirm'].format(s))

    context_data = await context.get_data()
    context_data['delete_ids'] = ','.join([str(item.id) for item in items_list])
    await context.set_data(context_data)
    return States.STATE_3_DELETE


# confirm delete
@dp.message_handler(lambda m: m.text.strip().lower() in ['да', 'yes'],
                    state=States.STATE_3_DELETE)
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def delete_confirm(uid,
                         context: FSMContext,
                         message: types.Message,
                         session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    # process delete
    context_data = await context.get_data()
    del_ids = context_data.get('delete_ids', None)
    _, _, del_records = sql_result(session.query(Item)
                                   .join(User)
                                   .filter(User.uid == uid)
                                   .filter(Item.id.in_(del_ids.split(','))))
    s = '\n'.join([x.row_repr() for x in del_records])
    for x in del_records:
        session.delete(x)
    reply_text = MESSAGES['delete_records_done'].format(s)
    context_data['delete_ids'] = None
    await context.set_data(context_data)
    await message.reply(reply_text)
    return States.STATE_1_MAIN


# /search
@dp.message_handler(state=States.STATE_4_SEARCH)
@add_middlewares(use_resolve_state=True,
                 use_db_session=True,
                 use_trace=True)
async def search_command(uid,
                         context,
                         message: types.Message,
                         session: sqlalchemy.orm.Session) -> Union[StateItem, None]:
    return States.STATE_1_MAIN


# /mycards
@dp.message_handler(commands=['mycards'],
                    state=States.STATE_1_MAIN)
@add_middlewares(use_db_session=True,
                 use_trace=True)
async def mycards(uid,
                  context,
                  message: types.Message,
                  session: sqlalchemy.orm.Session):
    args = message.get_args()

    _, user, _ = sql_result(session.query(User)
                            .filter(User.uid == uid))

    reply_text = Item.list_repr(user.owner_items)
    await message.reply(reply_text,
                        reply=False)
