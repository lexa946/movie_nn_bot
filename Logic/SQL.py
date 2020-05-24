import config
import pymysql
import socks, socket


def disable_tor(func):
    def wrapper(command, values=None):
        socks.set_default_proxy(None)
        socket.socket = socks.socksocket
        data = func(command, values)
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
        socket.socket = socks.socksocket
        return data
    return wrapper

@disable_tor
def execute_sql(command, values=None):
    """
    выполняет команду sql
    :param command: команда
    :return: вывод от команды
    """
    base = pymysql.connect(host=config.Base.host,
                           database=config.Base.database,
                           user=config.Base.user,
                           passwd=config.Base.passwd,
                           port=config.Base.port, )
    base.set_charset('utf8')
    try:
        with base.cursor() as cur:
            if values:
                cur.execute(command, values)
            else:
                cur.execute(command)
            response = cur.fetchall()
            base.commit()
    finally:
        base.close()
    return response

def get_state(id):
    """
    Выдает значение состояния по моду
    :param mode: если mode==user выдает состояние в котором сидит пользователь,
                    если mode==post выдает Выбранный в данный момент пост
    :param id: id пользователя
    :return: возвращает состояние
    """
    command = f'SELECT user_state, kino_state FROM users WHERE user_id = {id}'
    result = execute_sql(command)
    print(result)
    return result[0]

def set_state(mode, id, state):
    """
    назначаем состояние пользователя или поста
    :param mode: указываем user при изменении состояния пользователя,
                указываем kino при изменении состояния кино
    :param id: id поста или пользователя
    :param state: указываем новое состояние
    :return:
    """
    command = f'UPDATE users SET {mode}_state = {state} WHERE user_id = {id}'
    execute_sql(command)

def add_to_base(data):
    """
    добавление данных парсера в базу
    :param mode: выбираем таблицу
    :param data: словарь данных
    :return:
    """
    command = f'DELETE FROM kino'
    execute_sql(command)

    for i, item in enumerate(data):
        command = f'INSERT INTO kino VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        execute_sql(command,
                (i + 1, item["title"],
                 item["image"], item["rating"],
                 item["slogan"], item["url"],
                 item['trailer'],item['description'],
                 item['cinemas'],item['sessions'],))

def get_from_base(id_):
    command = 'SELECT name, img, rating, slogan, url, trailer, description, cinemas, sessions FROM kino WHERE id = %s'
    return execute_sql(command, (id_,))

if __name__ == '__main__':
    socks.set_default_proxy(None)
    socket.socket = socks.socksocket
