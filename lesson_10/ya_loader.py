import requests
from tqdm import tqdm
from time import sleep
from requests.exceptions import ConnectionError


class YaUploader:
    HOST = 'https://cloud-api.yandex.net'
    def __init__(self, token: str, path: str) -> None:
        self.token = token
        self.path = path

    def _get_headers(self) -> dict:
        """
        возвращает заголовки для запросов
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}',
        }

    def _mkdir(self) -> None:
        """
        Создаёт папку для загрузок
        """
        r = requests.put(url=f'{self.HOST}/v1/disk/resources?path={self.path}',
                         headers=self._get_headers())
        try:
            r.raise_for_status()
            print('Запрос успешно выполнен')
        except requests.exceptions.HTTPError as err:
            print(f'Произошла ошибка: {err}\nПапка не создана')

    def upload_file(self, files: dict) -> None:
        """
        перебирает словарь со ссылками и загружает их на ЯД
        """
        print(f'создаём папку {self.path}')
        self._mkdir()
        sleep(1)
        for name, link in tqdm(files.items()):
            try:
                params = {
                    'path': f'{self.path}/{name}.jpg',
                    'url': link['url']
                }
                requests.post(url=f'{self.HOST}/v1/disk/resources/upload/',
                            params=params, headers=self._get_headers())
            except Exception as e:
                print(f'файл {name} не был загружен')