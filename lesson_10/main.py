import json

from environs import Env

from vk_parser import VKParser
from ya_loader import YaUploader


def config(token: str, owner: str, album: str, ya_token: str) -> dict:
    env = Env()
    env.read_env()

    return {'access_token': env(token),
            'owner_id': env(owner),
            'album_id': env(album),
            'ya_token': env(ya_token)}

def decorator(func):
    def wrapper(*args, **kwargs):
        all_photos = func(*args, **kwargs)
        sorted_five: list[tuple] = sorted(all_photos.items(), reverse=True)[:5]
        return {f'{key[0]}_{key[1]}': value for key, value in sorted_five}
    return wrapper

@decorator
def get_photos(*args) -> dict:
    parse = VKParser(*args)
    parse.get()
    return parse.photos

def to_json(dct: dict) -> None:
    print('Дампим список в res.json()')
    to_json = [{'file_name': key, 'size': value['type']} for key, value in dct.items()]
    with open('resp.json', 'w') as out:
        json.dump(to_json, out)
    print('Проверьте resp.json')


if __name__ == '__main__':
    _config = config('access_token', 'owner_id', 'album_id', 'ya_token')
    if not all(_config.values()):
        for k, v in _config.items():
            if not v:
                while not v:
                    v = input(f'значение {k} не заполнено, ожидаю ввод: ')
                _config[k] = v
    photo_for_upload = get_photos(_config['access_token'],
                                  _config['owner_id'],
                                  _config['album_id'],)
    print('Загружаем файлы на ЯД')
    path_name = f'{_config["owner_id"]}_{_config["album_id"]}'
    uploader = YaUploader(token=_config["ya_token"], path=path_name)
    uploader.upload_file(photo_for_upload)
    to_json(photo_for_upload)
