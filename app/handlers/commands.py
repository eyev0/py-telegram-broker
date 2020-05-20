from aiogram import types

from app import dp
from app.handlers.util.states import States


@dp.message_handler(commands=['start'],
                    state='*')
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id, chat=message.from_user.id)
    await state.set_state(States.all()[0])
    await message.reply('Yo',
                        reply=False)
