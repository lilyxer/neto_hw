import requests


def get_file(URL):
    """URL - ссылка на скачивание
    Возвращаем JSON объект, если ответ получен
    """
    response = requests.get(url=URL)
    if response.status_code == 200:
        return response.json()
    