import functools

from aiogram.dispatcher import FSMContext
from aiogram.utils.helper import Helper, HelperMode, Item


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0_INITIAL = Item()
    STATE_1_UPLOAD = Item()
    STATE_2_VIEW = Item()
    STATE_3_DELETE = Item()


class CreateAccountStates(Helper):
    mode = HelperMode.snake_case

    CREATE_ACC_STATE_0_CITY = Item()
    CREATE_ACC_STATE_1_NAME = Item()
    CREATE_ACC_STATE_2_EMAIL = Item()
    CREATE_ACC_STATE_3_PHONE = Item()


def resolve_state(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)

        user_state: FSMContext = kwargs.get('user_state', None)
        if user_state is not None:
            await user_state.set_state(result)
        return result

    return decorator
