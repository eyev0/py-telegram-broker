import re
from typing import List, Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import any_state, default_state
from aiogram.types import ContentTypes, ReplyKeyboardRemove

import core.database.db_worker as db
from core import config
from core.bot import dp
from core.database.models import Item
from core.messages import MESSAGES
from core.utils.filters import filter_admin, filter_su, filter_user_inactive
from core.utils.states import States


def _parse_upload(
    raw_text: str,
    user_id: int,
    row_delimiter="\n",
    column_delimiter=",",
    trim_carriage_return=True,
) -> Union[List[Item], None]:
    result = []
    if trim_carriage_return:
        raw_text = raw_text.replace("\r", "")
    rows = raw_text.split(row_delimiter)
    for a in [row.split(column_delimiter) for row in rows]:
        if len(a) != 2:
            result = None
            break
        else:
            result.append(Item(user_id, name=a[0], price=a[1]))
    return result


def _parse_delete(raw_text: str, chat_id: int) -> Union[List, None]:
    if raw_text == "all":
        del_records = db.get_user_items(chat_id)
    else:
        if re.findall("[^0-9, ]", raw_text):
            return None
        del_ids = [x.strip() for x in raw_text.split(",")]
        del_records = db.get_user_items(chat_id, ids=del_ids)
    return del_records or []


def register_handlers():
    # check inactive
    @dp.message_handler(filter_user_inactive, state=any_state)
    async def inactive(message: types.Message):
        await message.reply(MESSAGES["user_inactive"], reply=False)
        await default_state.set()

    # /admin
    @dp.message_handler(filter_su, commands=["admin"], state=any_state)
    async def admin(message: types.Message):
        if not filter_admin(message):
            config.BOT_ADMINS.remove(message.from_user.id)
            await message.reply(MESSAGES["admin_enable"], reply=False)
        else:
            config.BOT_ADMINS.remove(message.from_user.id)
            await message.reply(MESSAGES["admin_disable"], reply=False)

    # /cancel
    @dp.message_handler(
        commands=["cancel"], state=[States.UPLOAD, States.DELETE, States.SEARCH],
    )
    async def cancel(message: types.Message):
        await message.reply(MESSAGES["cancel"])
        await default_state.set()

    # /start
    @dp.message_handler(commands=["start", "location"], state=any_state)
    async def start(message: types.Message):
        user = db.get_user(message.from_user.id)
        if not user.location or message.get_command() == "/location":
            await States.INITIAL_REQUEST_CITY.set()
            await message.reply(MESSAGES["request_postal_code"], reply=False)
        else:
            await default_state.set()

    # request city
    @dp.message_handler(
        state=States.INITIAL_REQUEST_CITY, content_types=ContentTypes.TEXT
    )
    async def request_city(message: types.Message):
        user = db.get_user(message.from_user.id)
        user.location = message.text
        await message.reply(
            MESSAGES["sign_up_complete"],
            reply=False,
            reply_markup=ReplyKeyboardRemove(),
        )
        await default_state.set()

    # /upload
    @dp.message_handler(commands=["upload"], state=default_state)
    async def upload_command(message: types.Message):
        await message.reply(MESSAGES["upload"])
        await States.UPLOAD.set()

    # process /upload
    @dp.message_handler(state=States.UPLOAD)
    async def upload_parse_rows(message: types.Message):
        user = db.get_user(message.from_user.id)
        upload_records = _parse_upload(message.text, user.id)
        if not upload_records:
            await message.reply(MESSAGES["upload_parse_failed"])
            await States.UPLOAD.set()
            return
        user_items = db.get_user_items(message.from_user.id)
        if len(upload_records) + len(user_items) > user.limit:
            await message.reply(
                MESSAGES["upload_limit_exceeded"].format(user.limit, message.text)
            )
            await default_state.set()
            return
        for item in upload_records:
            db.insert(item)
        await message.reply(MESSAGES["upload_complete"])
        await default_state.set()

    # /delete
    @dp.message_handler(commands=["delete"], state=default_state)
    async def delete_command(message: types.Message):
        # save del_ids and request confirmation
        args: str = message.get_args()
        context: FSMContext = dp.current_state(
            user=message.from_user.id, chat=message.chat.id
        )
        if len(args) == 0:
            await message.reply(MESSAGES["delete_help"])
            await default_state.set()
            return
        del_records = _parse_delete(args, message.from_user.id)
        if del_records is None:
            await message.reply(MESSAGES["delete_format_error"])
            await default_state.set()
            return
        if not del_records:
            await message.reply(MESSAGES["delete_no_records"])
            await default_state.set()
            return
        del_str = "\n".join([f"{item.row_repr()}" for item in del_records])
        await message.reply(MESSAGES["delete_records_confirm"].format(del_str))

        context_data = await context.get_data()
        context_data["delete_ids"] = ",".join([str(item.id) for item in del_records])
        await context.set_data(context_data)
        await States.DELETE.set()

    # confirm delete
    @dp.message_handler(
        lambda m: m.text.strip().lower() in ["да", "yes"], state=States.DELETE
    )
    async def delete_confirm(message: types.Message):
        # process delete
        context: FSMContext = dp.current_state(
            user=message.from_user.id, chat=message.chat.id
        )
        context_data = await context.get_data()
        del_ids = context_data.get("delete_ids", "")
        del_records = db.get_user_items(message.from_user.id, ids=del_ids)
        del_str = "\n".join([x.row_repr() for x in del_records])
        for item in del_records:
            db.delete(item)
        reply_text = MESSAGES["delete_records_done"].format(del_str)
        context_data["delete_ids"] = None
        await context.set_data(context_data)
        await message.reply(reply_text)
        await default_state.set()

    # /search
    @dp.message_handler(state=States.SEARCH)
    async def search_command(message: types.Message):
        await default_state.set()

    # /mycards
    @dp.message_handler(commands=["mycards"], state=default_state)
    async def mycards(message: types.Message):
        user = db.get_user(message.from_user.id)
        reply_text = Item.list_repr(user.owner_items)
        await message.reply(reply_text, reply=False)
