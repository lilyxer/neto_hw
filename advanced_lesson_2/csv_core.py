import requests

from csv import DictWriter


def load_csv(link: str, file_name: str) -> bool:
    """
    link - ссылка по которой будем скачивать файл
    file_name - имя для сохранения файла
    сохраняем csv файл по ссылке с гитхаба
    return True/False в зависимости от ответа
    """
    resp = requests.get(url=link)
    resp.encoding = 'utf-8'
    if resp.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(resp.content)
        return True
    return False

def write_lo_file(file_name: str, stroke: dict, fields: list[str]) -> None:
    """
    file_name - куда осуществляется дозапись файла
    stroke - словарь с данными
    fields - заголовки
    return None
    """
    with open(file_name, 'a') as file:
        writer = DictWriter(file, fields)
        writer.writerow(stroke)
        # print('запись добавлена')


if __name__ == '__main__':
    print(load_csv('https://raw.githubusercontent.com/netology-code/py-homeworks-advanced/master/5.Regexp/phonebook_raw.csv'))