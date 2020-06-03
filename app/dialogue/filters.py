import sqlalchemy.orm
from aiogram import types

from app import use_db_session, trace, sql_result, User


@use_db_session
def filter_account_created(message: types.Message, session: sqlalchemy.orm.Session):
    rowcount, user, _ = trace(sql_result)(session.query(User)
                                          .filter(User.uid == message.from_user.id))
    if user is None or user.location is None:
        return False
    return True
