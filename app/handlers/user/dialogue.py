import logging

from aiogram import types
from aiogram.types import ParseMode, ContentType

from app import dp
from app.db import session_scope
from app.db.models import User
from app.handlers.messages import MESSAGES
from app.handlers.states import States


@dp.message_handler(state=States.STATE_1,
                    content_types=ContentType.TEXT)
async def name(message: types.Message):
    uid = message.from_user.id
    with session_scope() as session:
        user = User(uid=uid,
                    username=message.from_user.username,
                    full_name=message.text) \
            .insert_me(session)
        logging.info(f'user created: {user}')

    await message.reply(MESSAGES['pleased_to_meet_you'],
                        parse_mode=ParseMode.MARKDOWN,
                        reply=False)


@dp.message_handler(state=States.all().append(None),
                    content_types=ContentType.ANY)
async def chat(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    current_state = await state.get_state()
    m_text = MESSAGES['help_' + str(current_state)]
    await message.reply(m_text,
                        reply=False)
