from aiogram import types

import app.database.db_worker as db
from app import config


def filter_user_inactive(message: types.Message):
    user = db.get_user(message.from_user.id)
    return not user.active


def filter_su(message: types.Message):
    return message.from_user.id in config.BOT_SU


def filter_admin(message: types.Message):
    return message.from_user.id in config.BOT_ADMINS
