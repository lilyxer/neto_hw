import json
import xml.etree.ElementTree as ET

class MyParser:
    def __init__(self) -> None:
        self.news_json: dict = {}
        self.news_xml: dict = {}

    def parse_xml(self, path: str) -> None:
        """
        считываем xml файл структурой == 'channel/item' и атрибутами title и description
        наполняем словарь экземпляра {'title': len('description')}
        """
        xl = ET.parse(path).getroot()
        for tag in xl.findall('channel/item'):
            title = tag.find('title').text
            desc = self._get_max_lens(tag.find('description').text)
            self.news_xml.update({title: desc})

    def parse_json(self, path: str) -> None:
        """
        считываем json файл структурой == {'rss': {'channel': {'items'}}} и полями title и description
        наполняем словарь экземпляра {'title': len('description')}
        """
        with open(path, 'r') as file:
            json_dict: dict = json.load(file)
            for elem in json_dict['rss']['channel']['items']:
                title = elem['title']
                desc = self._get_max_lens(elem['description'])
                self.news_json.update({title: desc})

    @staticmethod
    def _get_max_lens(stroke: str) -> int:
        """
        stroke: строка со статьей
        return: число слов в котором больше 6 символов
        """
        return sum(len(letter) > 6 for letter in stroke.split())

    @staticmethod
    def _get_top_ten(dictionary: dict) -> list[tuple]:
        """
        dictionary: словарь где ключ название статьи, значение число слов
        return: список топ-10 отсортированных кортежей по значению словаря
        """
        return sorted(dictionary.items(), key=lambda elem: elem[1], reverse=True)[:10]


    def top_ten_json(self) -> str:
        """
        Метод возвращает строку вида
        количество слов больше 6: <число слов>
        <название статьи>
        """
        top_ten = (
            f'количество слов больше 6: {news[1]}\n{news[0]}'
            for news in self._get_top_ten(self.news_json)
        )
        top_ten = "\n\n".join(top_ten)
        return f'в новостях топ 10 по длинне слов:\n{top_ten}'

    def top_ten_xml(self) -> str:
        """
        Метод возвращает строку вида
        количество слов больше 6: <число слов>
        <название статьи>
        """
        top_ten = (
            f'количество слов больше 6: {news[1]}\n{news[0]}'
            for news in self._get_top_ten(self.news_xml)
        )
        top_ten = "\n\n".join(top_ten)
        return f'в новостях топ 10 по длинне слов:\n{top_ten}'

    def __str__(self) -> str:
        return 'метод не определён, используйте top_ten_json() или top_ten_xml()'


if __name__ == '__main__':
    my_obj = MyParser()
    my_obj.parse_json('newsafr.json')
    my_obj.parse_xml('newsafr.xml')
    # print(my_obj.top_ten_json()) # выведет строку с топ 10 статей формата <кол-во слов> <имя статьи>, полученные из json файла
    # print(my_obj) # выведет подсказку для работы с объектом
    print(my_obj.news_json)
    print(my_obj.top_ten_json()==my_obj.top_ten_xml())