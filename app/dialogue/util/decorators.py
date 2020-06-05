import functools

from aiogram import types

from app import dp, bot
from app.trace import trace_async
from app.db.util import db_session
from app.dialogue.util.states import resolve_state


def add_handler_features(args_mode,
                         use_resolve_state=False,
                         use_db_session=False,
                         use_trace=False):
    arg_parsers = {
        'message': message_parse_args,
        'callback': callback_parse_args,
        'message_callback': message_callback_parse_args,
    }

    def decorator(func):
        if use_trace:
            func = trace_async(func)
        if use_db_session:
            func = db_session(func)
        if use_resolve_state:
            func = resolve_state(func)
        assert args_mode is not None
        assert args_mode in arg_parsers
        parse_func = arg_parsers[args_mode]
        func = parse_func(func)
        return func

    return decorator


def message_callback_parse_args(func):
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
            'callback_query': callback_query,
        }
        result = await func(**kwargs)
        if callback_query:
            await bot.answer_callback_query(callback_query.id)
        return result

    return decorator


def message_parse_args(func):
    @functools.wraps(func)
    async def decorator(message: types.Message, **partial_data):
        user_id = message.from_user.id
        context = partial_data.get('state', dp.current_state(user=user_id, chat=user_id))
        kwargs = {
            'user_id': user_id,
            'context': context,
            'message': message,
        }
        return await func(**kwargs)

    return decorator


def callback_parse_args(func):
    @functools.wraps(func)
    async def decorator(callback_query: types.CallbackQuery, **partial_data):
        message = callback_query.message
        user_id = callback_query.from_user.id
        context = partial_data.get('state', dp.current_state(user=user_id, chat=user_id))
        kwargs = {
            'user_id': user_id,
            'context': context,
            'message': message,
            'callback_query': callback_query,
        }
        result = await func(**kwargs)
        await bot.answer_callback_query(callback_query.id)
        return result

    return decorator
