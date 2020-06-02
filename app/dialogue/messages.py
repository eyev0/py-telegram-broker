greetings = 'Yo, давай знакомиться. В каком городе ты живешь?'
yo = 'Yo, как дела?'
help_ = ' '

enter_location = 'Yo, сначала укажи свой город'
sign_up_complete = 'Yo, отлично! Можешь заливать картон.'

upload = 'Yo, скинь мне список карт, которые хочешь загрузить. ' \
                        'Каждая строка должна иметь формат <Название>,<Цена>\n' \
                        'Например, так:\n\n' \
                        'Серый выхухоль,10\n' \
                        'Черная вдова,25\n' \
                        'Скрытный оползень,100\n' \
                        '...'
upload_code_inactive = 'Yo, ты в инактиве, друг! Ты не можешь загружать ничего, обратись в саппорт.'
upload_code_limit = 'Yo, твой лимит объявлений({}) превышен! Нельзя загрузить {} карт'
upload_complete = 'Yo, Успех!'

admin_enable = 'Ладно... будешь за админа теперь!'
admin_disable = 'Теперь ты как все, друг!'


MESSAGES = {
    # user messages
    'greetings': greetings,
    'yo': yo,
    'help_': help_,
    'enter_location': enter_location,
    'sign_up_complete': sign_up_complete,

    # admin messages
    'admin_enable': admin_enable,
    'admin_disable': admin_disable,

    # create event messages
    'upload': upload,
    'upload_code_inactive': upload_code_inactive,
    'upload_code_limit': upload_code_limit,
    'upload_complete': upload_complete,
}
