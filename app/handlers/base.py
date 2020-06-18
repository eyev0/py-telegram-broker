from aiogram import types
from aiogram.dispatcher.filters.state import any_state, default_state
from aiogram.types import ContentTypes, ReplyKeyboardRemove

from app.database import db_worker as db
from app.messages import MESSAGES
from app.misc import dp
from app.utils.filters import filter_user_inactive
from app.utils.states import States


@dp.message_handler(filter_user_inactive, state=any_state)
async def inactive(message: types.Message):
    await message.reply(MESSAGES["user_inactive"], reply=False)
    await default_state.set()


@dp.message_handler(
    commands=["cancel"], state=[States.UPLOAD, States.DELETE, States.SEARCH],
)
async def cancel(message: types.Message):
    await message.reply(MESSAGES["cancel"])
    await default_state.set()


@dp.message_handler(commands=["start", "location"], state=any_state)
async def start(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user.location or message.get_command() == "/location":
        await States.INITIAL_REQUEST_CITY.set()
        await message.reply(MESSAGES["request_postal_code"], reply=False)
    else:
        await default_state.set()


@dp.message_handler(state=States.INITIAL_REQUEST_CITY, content_types=ContentTypes.TEXT)
async def request_city(message: types.Message):
    user = db.get_user(message.from_user.id)
    user.location = message.text
    await message.reply(
        MESSAGES["sign_up_complete"], reply=False, reply_markup=ReplyKeyboardRemove(),
    )
    await default_state.set()
