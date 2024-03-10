from environs import Env


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
        'host': env('HOST'),
        'port': env('PORT')
    }