from typing import List, Union

import sqlalchemy.orm

from app.db import Session, sql_result
from app.db.models import Item, User

session: sqlalchemy.orm.Session = Session()


def insert(obj):
    session.add(obj)
    session.commit()
    return obj


def delete(obj):
    session.delete(obj)
    session.commit()


def get_user(uid) -> Union[User, None]:
    result = sql_result(session.query(User).filter(User.uid == uid))
    return result.one_row


def create_user(uid, username):
    insert(User(uid=uid, username=username))


def get_user_items(uid=None, ids=None) -> Union[List[Item], None]:
    get_all = ids is None or ids == "all"
    if isinstance(ids, str):
        ids = ids.split(",")
    user = get_user(uid)
    if user:
        if get_all:
            return user.owner_items
        else:
            _, _, items = sql_result(
                session.query(Item)
                .join(User)
                .filter(User.uid == uid)
                .filter(Item.id.in_(ids))
            )
            return items
    else:
        return None
