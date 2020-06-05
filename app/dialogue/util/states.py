import functools

from aiogram.dispatcher import FSMContext
from aiogram.utils.helper import Helper, HelperMode, Item


class StateItem(Item):
    pass


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0_REQUEST_CITY = StateItem()
    STATE_1_MAIN = StateItem()
    STATE_2_UPLOAD = StateItem()
    STATE_3_DELETE = StateItem()
    STATE_4_SEARCH = StateItem()
    STATE_5_VIEW = StateItem()


def resolve_state(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)

        context: FSMContext = kwargs.get('context', None)
        if context is not None:
            await context.set_state(result)
        return result

    return decorator
