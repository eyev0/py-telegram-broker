from aiogram import types
from aiogram.dispatcher.filters.state import default_state

from app.database import db_worker as db
from app.database.models import Item
from app.misc import dp
from app.utils.states import States


@dp.message_handler(state=States.SEARCH)
async def search_command(message: types.Message):
    await default_state.set()


@dp.message_handler(commands=["mycards"], state=default_state)
async def mycards(message: types.Message):
    user = db.get_user(message.from_user.id)
    reply_text = Item.list_repr(user.owner_items)
    await message.reply(reply_text, reply=False)
