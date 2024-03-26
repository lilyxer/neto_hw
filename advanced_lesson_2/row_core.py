import re

from csv import DictReader


def get_row(file: str):
    """
    file - ожидаем ссылку на csv файл
    создаём генератор чтобы не положить память компьютера
    return - возвращаем словарь
    """
    with open(file, 'r') as csv_file:
        yield from DictReader(csv_file)


def parce_row(dct: dict) -> dict:
    """
    dct - сырой словарь
    парсим словарь проверяем ключи с ФИО и телефоном
    return возращаем словарь
    """
    FIO = ['lastname', 'firstname', 'surname']
    if not all(map(dct.get, FIO)):
        tmp = []
        for elem in FIO:
            tmp.extend(dct.get(elem).split())
        for key, value in zip(FIO, tmp):
            dct[key] = value
    if phone:= dct.get('phone'):
        pattern = r'(\+7|8)[ -]?\(?(\d{3})\)?[ -]?\(?(\d{3})[ -]?(\d{2})[ -]?(\d{2})[\D]*(\d{4})?'
        s = re.search(pattern, phone)
        s = [x for x in s.groups() if x][1:]
        phone = ('+7({}){}-{}-{}'.format(*s)
                 if len(s) == 4 else
                 '+7({}){}-{}-{} доб.{}'.format(*s)
        )
        dct['phone'] = phone
    return dct