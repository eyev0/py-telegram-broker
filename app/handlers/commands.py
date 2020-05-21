from aiogram import types

from app import dp
from app.handlers.util.keyboards import keyboard_menu
from app.handlers.util.states import States


@dp.message_handler(commands=['start'],
                    state='*')
async def start(message: types.Message):
    uid = message.from_user.id
    state = dp.current_state(user=uid, chat=uid)
    await state.set_state(States.all()[0])
    await message.reply('Yo',
                        reply=False,
                        reply_markup=keyboard_menu)
