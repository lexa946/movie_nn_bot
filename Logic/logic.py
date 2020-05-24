from telebot import types
from Logic.message import Emoji
from Logic import SQL


def start(id):
    """
    Вызывается при первом включении бота и добавляет пользователя в базу
    :param id:
    :return:
    """
    command = f'SELECT * FROM users WHERE user_id={id}'
    user = SQL.execute_sql(command)
    print(user)
    if user:
        return True
    command = f'INSERT INTO users VALUES ({id}, 0, 0)'
    SQL.execute_sql(command)









if __name__ == '__main__':
    pass
    # mes = Message(1)
    # data = mes.data_kino
    # data_two = mes.data_more
    # print(1)