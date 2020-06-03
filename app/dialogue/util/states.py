import functools

from aiogram.dispatcher import FSMContext
from aiogram.utils.helper import Helper, HelperMode, Item


class StateItem(Item):
    pass


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0_INITIAL = StateItem()
    STATE_1_UPLOAD = StateItem()
    STATE_2_VIEW = StateItem()
    STATE_3_DELETE = StateItem()


class CreateAccountStates(Helper):
    mode = HelperMode.snake_case

    CREATE_ACC_STATE_0_CITY = StateItem()
    CREATE_ACC_STATE_1_NAME = StateItem()
    CREATE_ACC_STATE_2_EMAIL = StateItem()
    CREATE_ACC_STATE_3_PHONE = StateItem()


def resolve_state(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)

        user_state: FSMContext = kwargs.get('user_state', None)
        if user_state is not None:
            await user_state.set_state(result)
        return result

    return decorator
