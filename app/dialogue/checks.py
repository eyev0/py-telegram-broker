from typing import Tuple

import sqlalchemy.orm
from aiogram import types

from app import config
from app.dialogue.messages import MESSAGES
from app.dialogue.util.states import CreateAccountStates, States
from app.db import sql_result, use_db_session
from app.db.models import User, Card
from app.trace import trace


@use_db_session
def filter_account_created(message: types.Message, session: sqlalchemy.orm.Session):
    rowcount, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == message.from_user.id))
    if user.location is None:
        return False, CreateAccountStates.CREATE_ACC_STATE_0_CITY


def account_created(user: User) -> Tuple:
    if user.location is None:
        return False, CreateAccountStates.CREATE_ACC_STATE_0_CITY


def upload(user: User, upload_count: int, session: sqlalchemy.orm.Session) -> Tuple:
    if not user.active:
        return False, States.STATE_0_INITIAL, MESSAGES['upload_code_inactive']  # user inactive

    rowcount, row, rows = trace(sql_result)(session.query(Card)
                                            .filter(Card.owner_id == user.id)
                                            .filter(Card.status < 9))
    if upload_count + rowcount > user.limit:
        return False, States.STATE_0_INITIAL, MESSAGES['upload_code_limit']\
            .format(user.limit, upload_count)  # limit exceeded

    return True, States.STATE_1_UPLOAD, MESSAGES['upload']


def is_from_su(message: types.Message):
    return message.from_user.id in config.app.su


def is_from_admin(message: types.Message):
    return message.from_user.id in config.app.admin
