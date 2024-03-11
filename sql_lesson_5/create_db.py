import psycopg2


def create_database(_config):
    """
    Производим подключение к серверу базы, проверяем есть ли уже бд которую мы создаём,
    уточняем нужно ли её пересоздать
    """
    conn = psycopg2.connect(database = _config['db'],
                            user = _config['login'],
                            password = _config['password'],
                            host = _config['host'],
                            port = _config['port'])
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute("""CREATE DATABASE shop_db;""")
        print('[+] База данных shop_db создана')
    except Exception as e:
        print('[-] База данных vkinder_db была создана ранее')
        conn.rollback()
    conn.close()

if __name__ == '__main__':
    def config() -> dict:
        """
        получаем данные для работы с базой данных
        create_db - база данных которую будем дропать и создавать
        """
        from environs import Env


        env = Env()
        env.read_env()
        return {
            'login': env('USER_DB'),
            'password': env('PASSWORD'),
            'db': env('DATABASE'),
            'my_db': env('CREATE_DB'),
            'host': env('HOST'),
            'port': env('PORT')
        }


    conf = config()
    create_database(conf)