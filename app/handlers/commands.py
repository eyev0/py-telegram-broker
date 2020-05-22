from app import dp, bot
from app.decorators import cozy_args
from app.handlers.util.keyboards import *
from app.handlers.util.states import States
from app.log import trace_async


@dp.message_handler(commands=['start'],
                    state='*')
@trace_async
@cozy_args
async def start(user_id, message, user_state, **kwargs):
    uid = message.from_user.id
    state = dp.current_state(user=uid, chat=uid)
    await state.set_state(States.all()[0])
    await message.reply('Yo',
                        reply=False,
                        reply_markup=keyboard_menu)


@dp.callback_query_handler(lambda c: c.data == button_upload.callback_data,
                           state='*')
@dp.message_handler(commands=['upload'],
                    state='*')
@trace_async
@cozy_args
async def upload(user_id, message, user_state, is_callback, callback_query):
    await user_state.set_state(States.all()[0])
    await message.reply('Yo',
                        reply=False,
                        reply_markup=keyboard_menu)
    if is_callback:
        await bot.answer_callback_query(callback_query.id)
