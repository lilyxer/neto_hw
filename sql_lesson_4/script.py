import psycopg2
from environs import Env

from my_classes import MyBase


def create_database(_config):
    """
    Производим подключение к серверу базы, проверяем есть ли уже бд которую мы создаём,
    уточняем нужно ли её пересоздать
    """
    conn = psycopg2.connect(database = _config['db'],
                            user = _config['login'],
                            password = _config['password'],
                            host = _config['host'])
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""SELECT datname
                     FROM pg_catalog.pg_database;""")
    if 'clients_db' in [x[0] for x in cur.fetchall()]:
        answer = input('clients_db была создана ранее, '
                        'нужно ли её пересоздать? Y/N: ')
        if answer.casefold() == 'n':
            cur.close()
            conn.close()
            return
        cur.execute("""DROP DATABASE clients_db;""")
        print('clients_db была удалена')
    cur.execute("""CREATE DATABASE clients_db;""")
    print('clients_db была создана')
    cur.close()
    conn.close()
    return

def config() -> dict:
    """
    получаем данные для работы с базой данных
    create_db - база данных которую будем дропать и создавать
    """
    env = Env()
    env.read_env()
    return {
        'login': env('USER_DB'),
        'password': env('PASSWORD'),
        'db': env('DATABASE'),
        'my_db': env('CREATE_DB'),
        'host': env('HOST')
    }


if __name__ == '__main__':
    _config = config()
    create_database(_config)
    base = MyBase(dbname=_config['my_db'], user=_config['login'],
                  password=_config['password'], host=_config['host'])

    # создаём таблицы
    creates_query = ("""CREATE TABLE IF NOT EXISTS clients(
                        client_id SERIAL PRIMARY KEY,
                        f_name VARCHAR(20) NOT NULL,
                        l_name VARCHAR(30) NOT NULL,
                        email VARCHAR(30) NOT NULL UNIQUE);""",
                        """CREATE TABLE IF NOT EXISTS phones(
                        phone_id SERIAL PRIMARY KEY,
                        phone BIGINT UNIQUE NOT NULL,
                        client_id INT NOT NULL,
                        FOREIGN KEY (client_id) REFERENCES clients(client_id)
                        ON DELETE CASCADE);""")
    for q in creates_query:
        base.execute_query(query=q)

    first_name = ('Иван', 'Татьяна', 'Пётр', 'Пётр', 'Анастасия', 'Валентин', 'Тест',
                  'Тест2')
    last_name = ('Иванов', 'Самарина', 'Воронин', 'Воронин', 'Ермакова', 'Петров',
                 'Тестов', 'Тестов2')
    email = ('Ivanov@ya.ru', 'Samarina@ya.ru', 'Voronin@ya.ru', 'Voronin2@ya.ru',
             'Ermakova@ya.ru', 'Petrov@ya.ru', '@', None)
    phone = (89991112233, 89992223344, 89993334455, None, 89996667788, 89998889900,
             89998889900, None)


    for f_n, l_n, em, ph in zip(first_name, last_name, email, phone):
        print(base.add_new_client(f_name=f_n, l_name=l_n, email=em, phone=ph))

    print(base.add_phone(client_id=3, number=89997777777))
    print(base.add_phone(client_id=4, number=89991234567))
    print(base.add_phone(client_id=5, number=89996667788))
    print(base.add_phone(client_id=0, number=896667788))

    print(base.change_client(client_id=1, first_name='Ivan', last_name='Ivanov'))
    print(base.change_client(client_id=2))

    print(base.delete_phone(client_id=3, phone=89997777777))
    print(base.delete_phone(client_id=3, phone=89997777777))
    print(base.delete_phone(client_id=4, phone=89993334455))
    print(base.delete_phone(client_id=1, phone=000))

    print(base.delete_client(client_id=3))
    print(base.delete_client(client_id=3))

    if response := base.find_client(phone=89998889900):
        print(*response, sep='\n')
    else:
        print('Выборка не дала результата')

    print(base)
    base.close_connection()