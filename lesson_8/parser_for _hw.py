import json
import xml.etree.ElementTree as ET

from collections import Counter

class MyParser:
    def __init__(self) -> None:
        self.news_json: list = []
        self.news_xml: list = []

    def parse_xml(self, path: str) -> None:
        """
        считываем xml файл структурой == 'channel/item' и полями description
        наполняем список экземпляра словами из 'description' длинна которых больше 6
        """
        xl = ET.parse(path).getroot()
        for tag in xl.findall('channel/item'):
            self.news_xml.extend(el for el in tag.find('description').text.split() if len(el) > 6)

    def parse_json(self, path: str) -> None:
        """
        считываем json файл структурой == {'rss': {'channel': {'items'}}} и полями description
        наполняем список экземпляра словами из 'description' длинна которых больше 6
        """
        with open(path, 'r') as file:
            json_dict: dict = json.load(file)
            for elem in json_dict['rss']['channel']['items']:
                self.news_json.extend(el for el in elem['description'].split() if len(el) > 6)

    @staticmethod
    def get_top_ten(all_words: list) -> list:
        """
        return: список топ-10 отсортированных слов из списка по частоте появления
        """
        counter = Counter(all_words)
        return [word[0] for word in counter.most_common(10)]

    def __str__(self) -> str:
        return 'метод не определён, используйте get_top_ten(<список слов>)'


if __name__ == '__main__':
    my_obj = MyParser()
    my_obj.parse_json('newsafr.json')
    my_obj.parse_xml('newsafr.xml')
    # print(my_obj) # выведет подсказку для работы с объектом
    print(my_obj.get_top_ten(my_obj.news_json))
    print(my_obj.get_top_ten(my_obj.news_xml))
