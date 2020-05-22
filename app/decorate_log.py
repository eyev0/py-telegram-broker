import functools
import logging
from collections import Iterable

LVL_CALL = 25
logging.addLevelName(LVL_CALL, 'CALL')


def trace(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        logging.log(LVL_CALL,
                    f'TRACE: calling {func.__module__}.{func.__name__}(' +
                    f'{",".join([str(x) for x in args])}' +
                    ', ' +
                    f'{", ".join([str(x) + "=" + str(kwargs[x]) for x in kwargs])})')
        result = func(*args, **kwargs)

        if result is not None:
            if isinstance(result, Iterable):
                result_str = ', '.join([str(x) for x in result])
            else:
                result_str = result
            logging.log(LVL_CALL,
                        f'TRACE: {func.__module__}.{func.__name__} '
                        f'returned {result_str!r}')
        return result

    return decorator


def trace_async(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        logging.log(LVL_CALL,
                    f'TRACE: calling {func.__module__}.{func.__name__}(' +
                    f'{",".join([str(x) for x in args])}' +
                    ', ' +
                    f'{", ".join([str(x) + "=" + str(kwargs[x]) for x in kwargs])})')
        result = await func(*args, **kwargs)

        if result is not None:
            if isinstance(result, Iterable):
                result_str = ', '.join([str(x) for x in result])
            else:
                result_str = result
            logging.log(LVL_CALL,
                        f'TRACE: {func.__module__}.{func.__name__} '
                        f'returned {result_str!r}')
        return result

    return decorator
