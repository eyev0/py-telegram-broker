import functools
import logging
from typing import Iterable, Awaitable

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
                    f'TRACE: call {func.__module__}.{func.__name__}(' +
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
                        f'TRACE: return from {func.__module__}.{func.__name__}, '
                        f'returned {result_str!r}')
        return result

    return decorator


def trace_async(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        logging.log(config.log.trace_level,
                    f'TRACE: call {func.__module__}.{func.__name__}(' +
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
                        f'TRACE: return from {func.__module__}.{func.__name__}, '
                        f'returned {result_str!r}')
        return result

    return decorator


def db_session(func):
    """Add session kwarg"""

    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        with session_scope() as session:
            kwargs['session'] = session
            result = func(*args, **kwargs)
            if isinstance(result, Awaitable):
                result = await result
            return result

    return decorator


def sql_result(query: sqlalchemy.orm.Query,
               raise_on_empty_result=False):
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


def resolve_state(func):
    @functools.wraps(func)
    async def resolve_state_wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        context: FSMContext = kwargs.get('context', None)
        if context is not None:
            await context.set_state(result)
        return result

    return resolve_state_wrapper


def handler_args(mixed_mode=False):
    def decorator(func):

        @functools.wraps(func)
        async def handler_args_wrapper(obj: types.base.TelegramObject, **partial_data):
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

        return handler_args_wrapper

    return decorator


def add_middlewares(mixed_handler=False,
                    use_resolve_state=False,
                    use_db_session=False,
                    use_trace=False):
    def add_middlewares_wrapper(func):
        if use_trace:
            func = trace_async(func)
        if use_db_session:
            func = db_session(func)
        if use_resolve_state:
            func = resolve_state(func)
        func = handler_args(mixed_handler)(func)
        return func

    return add_middlewares_wrapper
