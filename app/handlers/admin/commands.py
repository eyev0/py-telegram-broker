from aiogram import types

from app import dp, config
from app.handlers.admin import show_events_task_admin
from app.handlers.keyboards import button_back_to_events
from app.handlers.lambdas import admin_lambda
from app.handlers.messages import MESSAGES
from app.handlers.states import MenuStates


@dp.message_handler(lambda m: m.text == button_back_to_events.text,
                    state=MenuStates.MENU_STATE_0)
@dp.message_handler(admin_lambda(),
                    state='*',
                    commands=['start'])
async def process_start_command_admin(message: types.Message):
    uid = message.from_user.id
    state = dp.current_state(user=uid)
    await state.set_state(MenuStates.all()[0])
    await show_events_task_admin(message)


@dp.message_handler(state='*',
                    commands=['admin'])
async def process_admin_command(message: types.Message):
    magic_word = message.get_args()
    uid = message.from_user.id
    state = dp.current_state(user=uid)
    if magic_word == 'pls':
        if uid not in config.admin_ids:
            config.admin_ids.append(uid)
            await state.set_state(None)
            await message.reply(MESSAGES['admin_enable'], reply=False)
    elif magic_word == 'no':
        if uid in config.admin_ids:
            config.admin_ids.remove(uid)
            await state.set_state(None)
            await message.reply(MESSAGES['admin_disable'], reply=False)
