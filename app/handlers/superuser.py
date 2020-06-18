from aiogram import types
from aiogram.dispatcher.filters.state import any_state

from app import config
from app.messages import MESSAGES
from app.misc import dp
from app.utils.filters import filter_admin, filter_su


@dp.message_handler(filter_su, commands=["admin"], state=any_state)
async def admin(message: types.Message):
    if not filter_admin(message):
        config.BOT_ADMINS.remove(message.from_user.id)
        await message.reply(MESSAGES["admin_enable"], reply=False)
    else:
        config.BOT_ADMINS.remove(message.from_user.id)
        await message.reply(MESSAGES["admin_disable"], reply=False)
