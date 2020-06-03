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
    STATE_3_VIEW = StateItem()
    STATE_4_DELETE = StateItem()


def resolve_state(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)

        user_state: FSMContext = kwargs.get('user_state', None)
        if user_state is not None:
            await user_state.set_state(result)
        return result

    return decorator
