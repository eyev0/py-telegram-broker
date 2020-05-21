greet_new_user = '*Привет!*\n' \
                 'Я - *Лера Трифонова*, а как вас зовут? Напишите, пожалуйста, *фамилию и имя* :)'
help_message = 'Это - *бот-помощник* для регистрации на онлайн-классы *Леры* *Трифоновой*\n' \
               'Введите /start, чтобы посмотреть список доступных мероприятий.\n' \
               'Если у вас есть вопрос про мероприятия или про этого бота - напишите мне *@danceleradance*'


admin_enable = 'Ладно... будешь за админа теперь!'
admin_disable = 'Теперь ты как все, друг!'
admin_restart = "Привет, админ! Введи /start, чтобы начать."
admin_record_deleted = 'Запись удалена!'

create_event_prompt_data_1 = 'Название мероприятия'
create_event_prompt_data_2 = 'Короткое описание мероприятия (или минус чтобы пропустить)'
create_event_prompt_data_3 = 'Отлично! Теперь напиши сообщение пользователю ' \
                             'об успешном завершении регистрации(не забудь вставить ссылку на канал)'
create_event_done = 'Готово!'
create_event_oops = 'Ой.'

MESSAGES = {
    # user messages
    'greet_new_user': greet_new_user,
    'help_message': help_message,

    # admin messages
    'admin_enable': admin_enable,
    'admin_disable': admin_disable,
    'admin_restart': admin_restart,
    'admin_record_deleted': admin_record_deleted,


    # create event messages
    'create_event_prompt_data_1': create_event_prompt_data_1,
    'create_event_prompt_data_2': create_event_prompt_data_2,
    'create_event_prompt_data_3': create_event_prompt_data_3,
    'create_event_done': create_event_done,
    'create_event_oops': create_event_oops,
}
