from app import dp, bot
from app.decorators import *
from app.handlers.util.keyboards import *
from app.handlers.util.states import States
from app.log import trace_async


@dp.message_handler(commands=['start'],
                    state='*')
@trace_async
@message_handler_cozy_args
async def start(user_id, message, user_state):
    await user_state.set_state(States.all()[0])
    await message.reply('Yo',
                        reply=False,
                        reply_markup=keyboard_menu)


@dp.callback_query_handler(lambda c: c.data == button_upload.callback_data,
                           state='*')
@dp.message_handler(commands=['upload'],
                    state='*')
@trace_async
@mixed_handler_cozy_args
async def upload(user_id, message, user_state, is_callback, callback_query):
    await user_state.set_state(States.all()[1])
    await message.reply('Upload',
                        reply=False)
    if is_callback:
        await bot.answer_callback_query(callback_query.id)
