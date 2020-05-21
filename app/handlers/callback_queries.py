from app import dp, bot
from app.handlers import States
from app.handlers.util.keyboards import *


@dp.callback_query_handler(lambda c: c.data == button_upload.callback_data,
                           state=States.STATE_0_INITIAL)
async def view_enrolls(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == button_view.callback_data,
                           state=States.STATE_0_INITIAL)
async def view_enrolls(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == button_delete.callback_data,
                           state=States.STATE_0_INITIAL)
async def view_enrolls(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
