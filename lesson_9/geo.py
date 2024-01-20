from environs import Env
import requests
from time import sleep

def config(token_name: str) -> str:
    env = Env()
    env.read_env()
    return env(token_name)

class MyGeo:
    URL = 'https://geocode.maps.co/reverse'
    def __init__(self, token: str) -> None:
        self.token = token
        self.cities = 'Leeds, London, Liverpool, Manchester, Oxford, Edinburgh, Norwich, York'.split(', ')

    def find_geo(self, coord: tuple[str]) -> str:
        set_of_geo = []
        for lat, long in coord:
            params = {
                'lat': lat,
                'lon': long,
                'api_key': self.token
            }
            resp = requests.get(url=self.URL, params=params)
            city = resp.json().get('address', {}).get('city')
            if city in self.cities:
                set_of_geo.append(city)
            sleep(1)
        return ', '.join(set_of_geo)


if __name__ == '__main__':
    token = config('geo_token')
    c = MyGeo(token)
    assert c.find_geo([('55.7514952', '37.618153095505875'),
        ('52.3727598', '4.8936041'),
        ('53.4071991', '-2.99168')]) == 'Liverpool'
