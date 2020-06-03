import functools
from typing import Tuple

import sqlalchemy.orm

from app.db import sql_result
from app.db.models import User, Card
from app.dialogue.messages import MESSAGES
from app.dialogue.util.states import States


def user_active(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        user = kwargs['user']
        if not user.active:
            result = False, None, MESSAGES['upload_code_inactive']  # user inactive
        else:
            result = func(*args, **kwargs)
        return result
    return decorator


@user_active
def upload(user: User = None, upload_count: int = 0, session: sqlalchemy.orm.Session = None) -> Tuple:
    rowcount, row, rows = sql_result(session.query(Card)
                                            .filter(Card.owner_id == user.id)
                                            .filter(Card.status < 9))
    if upload_count + rowcount > user.limit:
        return False, States.STATE_1_MAIN, MESSAGES['upload_code_limit']\
            .format(user.limit, upload_count)  # limit exceeded

    return True, States.STATE_1_MAIN, MESSAGES['upload_complete']
