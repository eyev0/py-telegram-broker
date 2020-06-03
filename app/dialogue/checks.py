import functools
from typing import Union, List

import sqlalchemy.orm

from app.db import sql_result
from app.db.models import User, Item
from app.dialogue.messages import MESSAGES
from app.dialogue.util.states import States


class CheckResult:
    def __init__(self,
                 reply_text,
                 passed=False,
                 next_state=States.STATE_1_MAIN,
                 data=None):
        self.passed = passed
        self.next_state = next_state
        self.reply_text = reply_text
        self.data = data

    def __repr__(self):
        return f'CheckResult(reply_text={self.reply_text}, passed={self.passed}, ' \
               f'state={self.next_state}, data={self.data})'


def user_active(user: User,
                passed_text='', passed_state=States.STATE_1_MAIN) -> CheckResult:
    if not user.active:
        return CheckResult(MESSAGES['upload_code_inactive'])  # user inactive
    return CheckResult(passed_text, passed=True, next_state=passed_state)


def user_active_wrapper(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        user = kwargs['user']
        if not user.active:
            result = CheckResult(MESSAGES['upload_code_inactive'])  # user inactive
        else:
            result = func(*args, **kwargs)
        return result
    return decorator


@user_active_wrapper
def upload(user: User = None, raw_text: str = None, session: sqlalchemy.orm.Session = None) -> CheckResult:
    items_list = parse_items(raw_text)
    if items_list is None:
        return CheckResult(MESSAGES['upload_parse_failed'])
    rowcount, row, rows = sql_result(session.query(Item)
                                     .filter(Item.owner_id == user.id)
                                     .filter(Item.status < 9))
    if len(items_list) + rowcount > user.limit:
        return CheckResult(MESSAGES['upload_limit_exceeded'].format(user.limit, raw_text))

    for item in items_list:
        Item(user.id, item['name'], item['price'])\
            .insert_me(session)
    return CheckResult(MESSAGES['upload_complete'], passed=True)


def parse_items(raw_text: str,
                row_delimiter='\n',
                column_delimiter=',',
                trim_carriage_return=True) -> Union[List, None]:
    result = []
    if trim_carriage_return:
        raw_text = raw_text.replace('\r', '')
    rows = raw_text.split(row_delimiter)
    for item in [row.split(column_delimiter) for row in rows]:
        if len(item) != 2:
            result = None
            break
        else:
            result.append({'name': item[0], 'price': item[1]})
    return result
