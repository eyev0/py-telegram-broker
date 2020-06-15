import functools
import logging
from collections import namedtuple
from contextlib import contextmanager
from typing import Awaitable

import sqlalchemy.orm
from sqlalchemy.orm import scoped_session, sessionmaker

from core import config
from core.database.models import Base

engine = sqlalchemy.create_engine(config.db.connect_str)

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class SQLEmptyResultError(Exception):
    """Raise when at least one row is expected"""

    pass


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session: sqlalchemy.orm.Session = Session()
    try:
        yield session
        session.commit()
    except SQLEmptyResultError:
        logging.exception("Got unexpected empty result for query:")
        session.rollback()
        pass
    except Exception:
        logging.exception("Got Error From Database:")
        session.rollback()
        raise
    finally:
        session.close()


def with_session(func):
    """Add session kwarg"""

    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        with session_scope() as session:
            kwargs["session"] = session
            result = func(*args, **kwargs)
            if isinstance(result, Awaitable):
                result = await result
            return result

    return decorator


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
    result = namedtuple("SQLResult", ["rowcount", "one_row", "rows_list"])
    return result(rowcount, first_row, rows_list)
