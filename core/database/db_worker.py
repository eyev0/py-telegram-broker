from typing import List, Union

import sqlalchemy.orm

from core.database import Session, sql_result
from core.database.models import Item, User

session: sqlalchemy.orm.Session = Session()


def on_shutdown(dp):
    session.commit()
    session.close()


def insert(obj):
    session.add(obj)
    session.commit()
    return obj


def delete(obj):
    session.delete(obj)
    session.commit()


def get_user(chat_id) -> Union[User, None]:
    result = sql_result(session.query(User).filter(User.chat_id == chat_id))
    return result.one_row


def update_user(chat_id, first_name, last_name, username):
    user = get_user(chat_id)
    if user is None:
        new_user = User(
            chat_id=chat_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        session.add(new_user)
        session.commit()
    else:
        user.chat_id = chat_id
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        session.commit()


def create_user(chat_id, username):
    insert(User(chat_id=chat_id, username=username))


def get_user_items(chat_id=None, ids=None) -> Union[List[Item], None]:
    get_all = ids is None or ids == "all"
    if isinstance(ids, str):
        ids = ids.split(",")
    user = get_user(chat_id)
    if user:
        if get_all:
            return user.owner_items
        else:
            _, _, items = sql_result(
                session.query(Item)
                .join(User)
                .filter(User.chat_id == chat_id)
                .filter(Item.id.in_(ids))
            )
            return items
    else:
        return None
