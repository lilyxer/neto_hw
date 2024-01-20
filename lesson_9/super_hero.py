import requests

from dataclasses import dataclass, field

@dataclass(order=True, slots=True)
class MyHero:
    name: str = field(compare=False)
    intelligence: int

    def __str__(self) -> str:
        return f'{self.name}'

    __repr__  = __str__

class MyParser:
    BASE_URL = 'https://akabab.github.io/superhero-api/api'

    def __init__(self) -> None:
        self.founded_hero: list[MyHero] = []

    # def _parse_json(self, obj)
    def get_response(self, look_for_hero: tuple[str], route: str='') -> None:
        url = f'{self.BASE_URL}{route}'
        if route == '/all.json':
            resp = requests.get(url)
            if resp.status_code == 200:
                all_heroes = resp.json()
                cnt = 0
                for hero in all_heroes:
                    if cnt == len(look_for_hero):
                        break
                    if hero['name'] in look_for_hero:
                        self.founded_hero.append(MyHero(name = hero['name'],
                                                        intelligence = hero['powerstats']['intelligence']))
            else:
                print('somethg wrong:/')
        elif route == '/id':
            for _id in look_for_hero:
                resp = requests.get(f'{url}/{_id}.json')
                if resp.status_code == 200:
                    hero = resp.json()
                    self.founded_hero.append(MyHero(name = hero['name'],
                                                        intelligence = hero['powerstats']['intelligence']))

def get_the_smartest_superhero(lst):
    my_heroes = MyParser()
    my_heroes.get_response(lst, route='/id')
    return str(max(my_heroes.founded_hero))


if __name__ == '__main__':
    # # создаём объект парсера
    # my_heroes = MyParser()
    # # вызываем метод для парсинга героев
    # # my_heroes.get_response('Hulk', 'Captain America', 'Thanos')
    # # выводим имя героя с максимальным интеллектом
    # # print(type(str(max(my_heroes.founded_hero))))
    # my_heroes.get_response(1,23, route='/id')
    # print(max(my_heroes.founded_hero))
    print(get_the_smartest_superhero((332, 149, 655)))