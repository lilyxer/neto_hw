import json
import xml.etree.ElementTree as ET

class MyParser:
    def __init__(self) -> None:
        self.news_json: dict = {}
        self.news_xml: dict = {}

    @staticmethod
    def _get_max_lens(stroke: str) -> int:
        return sum(1 if len(letter) > 6 else 0 for letter in stroke.split())

    def parse_xml(self, path: str) -> None:
        xl = ET.parse(path).getroot()
        for tag in xl.findall('channel/item'):
            title = tag.find('title').text
            desc = self._get_max_lens(tag.find('description').text)
            self.news_xml.update({title: desc})

    def parse_json(self, path: str) -> None:
        with open(path, 'r') as file:
            json_dict: dict = json.load(file)
            for elem in json_dict['rss']['channel']['items']:
                title = elem['title']
                desc = self._get_max_lens(elem['description'])
                self.news_json.update({title: desc})

    def top_ten_json(self) -> str:
        top_ten = [
            f'количество слов больше 6: {self._get_max_lens(news["description"])}\nназвание статьи: {news["title"]}'
            for news in self.news_json[:10]
        ]
        top_ten = "\n\n".join(top_ten)
        return f'в новостях топ 10 по длинне слов:\n{top_ten}'

    def __str__(self) -> str:
        return 'метод не определён, используйте top_ten_json или top_ten_xml'


if __name__ == '__main__':
    json_obj = MyParser()
    # json_obj.parse_json('newsafr.json')
    json_obj.parse_xml('newsafr.xml')
    # print(json_obj.top_ten_json()) # выведет строку с топ 10 статей формата <кол-во слов> <имя статьи>
    # print(json_obj) # выведет подсказку для работы с объектом
    # print(json_obj.parse_xml())
    print(json_obj.news_xml)