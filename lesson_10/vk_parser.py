from environs import Env
from requests.exceptions import ConnectionError
from tqdm import tqdm
from time import sleep
import requests


def config(token: str, owner: str, album: str) -> dict:
    env = Env()
    env.read_env()

    return {'access_token': env(token),
            'owner_id': env(owner),
            'album_id': env(album)}


class VKParser:
    URL = 'https://api.vk.com/method/photos.get'
    SIZES = dict(zip(('s', 'm', 'o', 'p', 'q', 'r', 'x', 'y', 'z', 'w'), range(1, 11)))

    def __init__(self, token: str, id_: int, album: str = 'profile') -> None:
        self.token = token
        self.id_ = id_
        self.album = album
        self.photos = {}

    def _get_max_size(self, photo: dict) -> None:
        """из словаря получаем дату, лайки и ссылку с максиальным разрешением фото
        используя словарь SIZES
        полученные данные записываем в словарь
        self.photos[лайк_дата] = ссылка
        """
        date = photo.get('date', 0)
        like = photo.get('likes', {}).get('count', 0)
        self.photos[(like, date)] = max(photo.get('sizes'), key=lambda x: self.SIZES[x['type']])['url']

    def get(self):
        params = {
            'access_token': self.token,
            'owner_id': self.id_,
            'album_id': self.album,
            'extended': True,
            'v': 5.199,
        }
        resp = requests.get(url=self.URL, params=params)
        try:
            resp.raise_for_status
            if e := resp.json().get('error', {}).get('error_msg'):
                raise ConnectionError(e)
            print('получаем фотографии с ВК')
            for x in tqdm(resp.json().get('response', {}).get('items')):
                self._get_max_size(x)
                sleep(0.2)
        except ConnectionError as e:
            print('Сервер вернул ошибку')
            raise e

if __name__ == '__main__':
    my_ = config('access_token', 'owner_id', 'album_id')
    if not all(my_.values()):
        for k, v in my_.items():
            if not v:
                while not v:
                    v = input(f'значение {k} не заполнено, ожидаю ввод: ')
                my_[k] = v
    parse = VKParser(*my_.values())
    parse.get()
    # print(parse.photos)