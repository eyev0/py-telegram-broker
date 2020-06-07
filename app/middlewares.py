import functools
import logging
from typing import Iterable

import sqlalchemy.orm
from aiogram import types
from aiogram.dispatcher import FSMContext

from app import config, dp, bot
from app.db import session_scope, SQLEmptyResultError

if config.log.add_trace_level_name:
    logging.addLevelName(config.log.trace_level, 'TRACE')


def trace(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        logging.log(config.log.trace_level,
                    f'TRACE: calling {func.__module__}.{func.__name__}(' +
                    f'{",".join([str(x) for x in args])}' +
                    ', ' +
                    f'{", ".join([str(x) + "=" + str(kwargs[x]) for x in kwargs])})')
        result = func(*args, **kwargs)

        if result is not None:
            if isinstance(result, Iterable) and not isinstance(result, str):
                result_str = ', '.join([str(x) for x in result])
            else:
                result_str = result
            logging.log(config.log.trace_level,
                        f'TRACE: {func.__module__}.{func.__name__} '
                        f'returned {result_str!r}')
        return result

    return decorator


def trace_async(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        logging.log(config.log.trace_level,
                    f'TRACE: calling {func.__module__}.{func.__name__}(' +
                    f'{",".join([str(x) for x in args])}' +
                    ', ' +
                    f'{", ".join([str(x) + "=" + str(kwargs[x]) for x in kwargs])})')
        result = await func(*args, **kwargs)

        if result is not None:
            if isinstance(result, Iterable) and not isinstance(result, str):
                result_str = ', '.join([str(x) for x in result])
            else:
                result_str = result
            logging.log(config.log.trace_level,
                        f'TRACE: {func.__module__}.{func.__name__} '
                        f'returned {result_str!r}')
        return result

    return decorator


def db_session(func):
    """Add session kwarg"""

    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        with session_scope() as session:
            kwargs['session'] = session
            return await func(*args, **kwargs)

    return decorator


def resolve_state(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)
        context: FSMContext = kwargs.get('context', None)
        if context is not None:
            await context.set_state(result)
        return result

    return decorator


def handler_args(mixed_mode=False):
    def handler_args_wrapper(func):
        """ Parse args for message and callback_query handlers in one func"""

        @functools.wraps(func)
        async def decorator(obj: types.base.TelegramObject, **partial_data):
            callback_query = None
            if isinstance(obj, types.CallbackQuery):
                callback_query = obj
                message = obj.message
                user_id = callback_query.from_user.id
            elif isinstance(obj, types.Message):
                message = obj
                user_id = message.from_user.id
            else:
                return
            context = partial_data.get('state', dp.current_state(user=user_id, chat=user_id))

            kwargs = {
                'user_id': user_id,
                'context': context,
                'message': message,
            }
            if callback_query and mixed_mode:
                kwargs['callback_query'] = callback_query

            result = await func(**kwargs)
            if callback_query:
                await bot.answer_callback_query(callback_query.id)
            return result

        return decorator

    return handler_args_wrapper


def add_middlewares(mixed_handler=False,
                    use_resolve_state=False,
                    use_db_session=False,
                    use_trace=False):
    def decorator(func):
        if use_trace:
            func = trace_async(func)
        if use_db_session:
            func = db_session(func)
        if use_resolve_state:
            func = resolve_state(func)
        func = handler_args(mixed_handler)(func)
        return func

    return decorator


@trace
def sql_result(query: sqlalchemy.orm.Query, raise_on_empty_result=False):
    """Return rowcount, first row and rows list for query"""
    rowcount = query.count()
    if rowcount > 0:
        rows_list = query.all()
        first_row = query.one()
    else:
        rows_list = first_row = None

    if raise_on_empty_result and rowcount == 0:
        raise SQLEmptyResultError()
    return rowcount, first_row, rows_list
