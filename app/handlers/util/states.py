from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0_INITIAL = ListItem()
    STATE_1_UPLOAD = ListItem()
    STATE_2_VIEW = ListItem()
    STATE_3_DELETE = ListItem()
