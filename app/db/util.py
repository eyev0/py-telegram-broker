import functools
import logging
from contextlib import contextmanager

import sqlalchemy.orm

from app.db import Session
from app.trace import trace


class Direction(object):
    REWIND_BACK = '<<'
    REWIND_FORWARD = '>>'
    BACK = ['<', '-']
    FORWARD = ['>', '+']
    map = {

    }

    @staticmethod
    def is_rewind(data):
        return len(data) > 1

    def __init__(self, data: str):
        self.direction = data
        self.rewind = self.is_rewind(data)
        self.back = data[-1:] in self.BACK
        self.forward = data[-1:] in self.FORWARD


def fetch_list(list_: list,
               current_pos: int,
               do_scroll=False,
               where: str = None):
    if len(list_) == 0:
        return None
    if do_scroll:
        direction = Direction(where)
        if direction.rewind:
            current_pos = (len(list_) - 1 if direction.forward else 0)
        else:
            current_pos += (1 if direction.forward else -1)
    # wrap around list
    if current_pos > len(list_) - 1:
        current_pos = 0
    elif current_pos < 0:
        current_pos = len(list_) - 1

    return list_[current_pos], current_pos


class WrappingListIterator(object):
    pass


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session: sqlalchemy.orm.Session = Session()
    try:
        yield session
        session.commit()
    except SQLEmptyResultError:
        logging.exception('Got unexpected empty result for query:')
        session.rollback()
        pass
    except Exception:
        logging.exception('Got Error From Database:')
        session.rollback()
        raise
    finally:
        session.close()


def db_session(func):
    """Add session kwarg to this function call"""
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        with session_scope() as session:
            kwargs['session'] = session
            return await func(*args, **kwargs)
    return decorator


class SQLEmptyResultError(Exception):
    """Raise when at least one row is expected"""
    pass


@trace
def sql_result(query: sqlalchemy.orm.Query, raise_on_empty_result=False):
    """Return rowcount, first row and rows list for query"""
    rowcount = query.count()
    if rowcount > 0:
        rows_list = query.all()
        first_row = rows_list[0]
    else:
        rows_list = first_row = None

    if raise_on_empty_result and rowcount == 0:
        raise SQLEmptyResultError()
    return rowcount, first_row, rows_list
