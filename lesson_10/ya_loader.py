from environs import Env
import requests
import os


def config(token_name: str) -> str:
    env = Env()
    env.read_env()
    return env(token_name)


class YaUploader:
    HOST = 'https://cloud-api.yandex.net'

    def __init__(self, token: str) -> None:
        self.token = token

    def _get_headers(self) -> dict:
        """
        возвращает заголовки для запросов
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}',
        }

    def _mkdir(self, path: str) -> None:
        """
        Создаёт папку для загрузок
        path: относительный путь к папке с файлами
        return: None - оповещание о статусе операции
        """
        r = requests.put(url=f'{self.HOST}/v1/disk/resources?path={path}',
                         headers=self._get_headers())
        try:
            r.raise_for_status()
            print('Запрос успешно выполнен')
        except requests.exceptions.HTTPError as err:
            print(f'Произошла ошибка: {err}\nПапка не создана')

    def _get_url(self, relative_path: str) -> str|None:
        """
        relative_path: str относительный путь к файлу
        метод возвращает ссылку для загрузки файла на я.диск
        """
        params = {
            'path': relative_path,
            'owerwrite': True,
        }
        header = self._get_headers()
        resp = requests.get(url=f'{self.HOST}/v1/disk/resources/upload/',
                            headers=header, params=params)
        try:
            resp.raise_for_status()
            return resp.json()['href']
        except requests.exceptions.HTTPError as err:
            print(f'Произошла ошибка: {err}\nСсылку получить не удалось')

    def _upload_file(self, full_path: str, relative_path: str) -> None:
        """
        full_path: str полный путь к файлу - необходим для открытия файла на компьютере
        relative_path: str относительноый путь необходимо знать только нижнюю папку что бы загрзить на я.диск
        return: сообщение о статусе загрузки файла
        """
        url = self._get_url(relative_path)
        with open(full_path, 'rb') as img:
            href = requests.put(url=url, data=img)
            try:
                href.raise_for_status()
                print(full_path, 'upload')
            except requests.exceptions.HTTPError as err:
                print(f'Произошла ошибка: {err}\nфайл загрузить не удалось')

    def upload(self, path: str) -> None:
        """
        Метод для загрузки фото на ваш я.диск
        path - путь к файлам на компьютере
        поочередно:
            - создает директорию на я.диске: _mkdir
            - проверяем файлы в директории
            - передаём в загрузчик
        """
        directory = path.split('/')[-1]
        self._mkdir(path=directory)
        for file in os.listdir(path=path):
            full_path = os.path.join(path, file)
            relative_path = os.path.join(directory, file)
            self._upload_file(full_path, relative_path)

if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = '/home/lilyxer/Изображения/to_ya_disc'
    YA_TOKEN = config('ya_token')
    uploader = YaUploader(YA_TOKEN)
    uploader.upload(path_to_file)
