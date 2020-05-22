import functools

from aiogram.dispatcher import FSMContext
from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0_INITIAL = ListItem()
    STATE_1_UPLOAD = ListItem()
    STATE_2_VIEW = ListItem()
    STATE_3_DELETE = ListItem()


class CreateAccountStates(Helper):
    mode = HelperMode.snake_case

    CREATE_ACC_STATE_0_CITY = ListItem()
    CREATE_ACC_STATE_1_NAME = ListItem()
    CREATE_ACC_STATE_2_EMAIL = ListItem()
    CREATE_ACC_STATE_3_PHONE = ListItem()


def resolve_state(func):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)

        user_state: FSMContext = kwargs.get('user_state', None)
        if user_state is not None:
            await user_state.set_state(result)
        return result

    return decorator
