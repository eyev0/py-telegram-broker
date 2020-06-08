greetings = 'Давай знакомиться. Для начала напиши, в каком городе ты живешь, ' \
            'чтобы я мог зарегистрировать тебя в базе пользователей нашей площадки.'
sign_up_complete = 'Отлично! Можешь заливать картон.'
yo = 'Как дела?'
help_ = ' '

user_inactive = 'Ты в инактиве, друг! Обратись в саппорт.'

cancel = 'Текущее действие отменено'

upload = 'Скинь мне список карт, которые хочешь загрузить. ' \
         'Каждая строка должна иметь формат <Название>,<Цена>\n' \
         'Например, так:\n\n' \
         'Серый выхухоль,10\n' \
         'Черная вдова,25\n' \
         'Скрытный оползень,100\n' \
         '...'
upload_parse_failed = 'Что-то не так с форматом твоего списка.. Не могу распарсить твой запрос на добавление. ' \
                      'Приведи все к формату выше.'
upload_limit_exceeded = 'Твой лимит объявлений({}) превышен! Нельзя загрузить {} карт'
upload_complete = 'Успех!'

delete_help = 'Что ты хочешь удалить? Пришли список id через пробел.\n' \
              'Например, /delete 10 1 3 22'
delete_format_error = 'Не, не так..\n' + delete_help
delete_no_records = 'Нет карт с такими id!\n' \
                    'Напиши /mycards, чтобы посмотреть список своих карт'
delete_records_confirm = 'You are about to delete these records:\n' \
                         '{}\n' \
                         'Type in "да/yes" to confirm or /cancel to cancel'
delete_cancelled = 'Delete cancelled'
delete_records_done = 'Records:\n{}\ndeleted!'

search = 'Что ты хочешь найти?'

admin_enable = 'Ладно... будешь за админа теперь!'
admin_disable = 'Теперь ты как все, друг!'

MESSAGES = {
    # user messages
    'greetings': greetings,
    'yo': yo,
    'help_': help_,
    'sign_up_complete': sign_up_complete,

    # admin messages
    'admin_enable': admin_enable,
    'admin_disable': admin_disable,

    # errors
    'user_inactive': user_inactive,
    'upload_parse_failed': upload_parse_failed,
    'upload_limit_exceeded': upload_limit_exceeded,

    'cancel': cancel,

    # upload messages
    'upload': upload,
    'upload_complete': upload_complete,

    # delete messages
    'delete_help': delete_help,
    'delete_format_error': delete_format_error,
    'delete_no_records': delete_no_records,
    'delete_records_confirm': delete_records_confirm,
    'delete_cancelled': delete_cancelled,
    'delete_records_done': delete_records_done,

    # search messages
    'search': search,
}

# YO!
for key in MESSAGES:
    MESSAGES[key] = 'Yo, ' + MESSAGES[key]
