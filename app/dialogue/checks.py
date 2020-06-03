import functools
from typing import Tuple, Union, List

import sqlalchemy.orm

from app.db import sql_result
from app.db.models import User, Item
from app.dialogue.messages import MESSAGES
from app.dialogue.util.states import States


def user_active(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        user = kwargs['user']
        if not user.active:
            result = False, States.STATE_1_MAIN, MESSAGES['upload_code_inactive']  # user inactive
        else:
            result = func(*args, **kwargs)
        return result
    return decorator


@user_active
def upload(user: User = None, raw_text: str = None, session: sqlalchemy.orm.Session = None) -> Tuple:
    items_list = parse_items(raw_text)
    if items_list is None:
        return False, States.STATE_1_MAIN, MESSAGES['upload_parse_failed']
    rowcount, row, rows = sql_result(session.query(Item)
                                     .filter(Item.owner_id == user.id)
                                     .filter(Item.status < 9))
    if len(items_list) + rowcount > user.limit:
        return False, States.STATE_1_MAIN, MESSAGES['upload_limit_exceeded'].format(user.limit, raw_text)

    return True, States.STATE_1_MAIN, MESSAGES['upload_complete']


def parse_items(text: str) -> Union[List, None]:
    rows = text.split('\n')
    result = []
    for card in [x.split(',') for x in rows]:
        if len(card) != 2:
            result = None
            break
        else:
            result.append({'name': card[0], 'price': card[1]})
    return result
