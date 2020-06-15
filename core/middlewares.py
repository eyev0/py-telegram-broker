import functools
import logging
from typing import Iterable

from aiogram import types
from aiogram.dispatcher import FSMContext

from core import bot, config, dp

if config.log.add_trace_level_name:
    logging.addLevelName(config.log.trace_level, "TRACE")


def trace(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        args_str = ",".join([str(x) for x in args])
        kwargs_str = ", ".join([str(k) + "=" + str(v) for k, v in kwargs.items()])
        logging.log(
            config.log.trace_level,
            f"TRACE: call {func.__module__}.{func.__name__}("
            + f"{args_str}"
            + ", "
            + f"{kwargs_str})",
        )
        result = func(*args, **kwargs)

        if result is not None:
            if isinstance(result, Iterable) and not isinstance(result, str):
                result_str = ", ".join([str(x) for x in result])
            else:
                result_str = result
            logging.log(
                config.log.trace_level,
                f"TRACE: return from {func.__module__}.{func.__name__}, "
                f"returned {result_str!r}",
            )
        return result

    return decorator


def trace_async(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        args_str = ",".join([str(x) for x in args])
        kwargs_str = ", ".join([str(k) + "=" + str(v) for k, v in kwargs.items()])
        logging.log(
            config.log.trace_level,
            f"TRACE: call {func.__module__}.{func.__name__}("
            + f"{args_str}"
            + ", "
            + f"{kwargs_str})",
        )
        result = await func(*args, **kwargs)

        if result is not None:
            if isinstance(result, Iterable) and not isinstance(result, str):
                result_str = ", ".join([str(x) for x in result])
            else:
                result_str = result
            logging.log(
                config.log.trace_level,
                f"TRACE: return from {func.__module__}.{func.__name__}, "
                f"returned {result_str!r}",
            )
        return result

    return decorator


def resolve_state(func):
    """Deprecated"""

    @functools.wraps(func)
    async def resolve_state_wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        context: FSMContext = kwargs.get("context", None)
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
                uid = callback_query.from_user.id
            elif isinstance(obj, types.Message):
                message = obj
                uid = message.from_user.id
            else:
                return
            context = partial_data.get("state", dp.current_state(user=uid, chat=uid))

            kwargs = {
                "uid": uid,
                "context": context,
                "message": message,
            }
            if callback_query and mixed_mode:
                kwargs["callback_query"] = callback_query

            result = await func(**kwargs)
            if callback_query:
                await bot.answer_callback_query(callback_query.id)
            return result

        return handler_args_wrapper

    return decorator


def add_handler_middlewares(mixed_handler=False, use_trace=False):
    def add_middlewares_wrapper(func):
        if use_trace:
            func = trace_async(func)
        func = handler_args(mixed_handler)(func)
        return func

    return add_middlewares_wrapper
