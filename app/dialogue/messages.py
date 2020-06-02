greetings = 'Yo, давай знакомиться. В каком городе ты живешь?'
help_message = ' '


upload = 'Yo, скинь мне список карт, которые хочешь загрузить. ' \
                        'Каждая строка должна иметь формат <Название>,<Цена>\n' \
                        'Например, так:\n\n' \
                        'Серый выхухоль,10\n' \
                        'Черная вдова,25\n' \
                        'Скрытный оползень,100\n' \
                        '...'
upload_code_inactive = 'Yo, ты в инактиве, друг! Ты не можешь загружать ничего, обратись в саппорт.'
upload_code_limit = 'Yo, твой лимит объявлений({}) превышен! Нельзя загрузить {} карт'

admin_enable = 'Ладно... будешь за админа теперь!'
admin_disable = 'Теперь ты как все, друг!'


MESSAGES = {
    # user messages
    'greet_new_user': greetings,
    'help_message': help_message,

    # admin messages
    'admin_enable': admin_enable,
    'admin_disable': admin_disable,

    # create event messages
    'upload': upload,
    'upload_code_inactive': upload_code_inactive,
    'upload_code_limit': upload_code_limit,
}
