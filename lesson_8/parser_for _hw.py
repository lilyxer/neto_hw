import json


class MyParser:
    def __init__(self) -> None:
        self.news_json: list

    @staticmethod
    def _get_max_lens(stroke: str) -> int:
        return sum(1 if len(letter) > 6 else 0 for letter in stroke.split())

    def parse_json(self, path: str) -> None:
        with open(path, 'r') as file:
            json_dict: dict = json.load(file)
            self.news_json = json_dict['rss']['channel']['items']
            self.news_json.sort(key=lambda elem: self._get_max_lens(elem['description']), reverse=True)

    def top_ten_json(self) -> str:
        top_ten = [
            f'количество слов  больше 6: {self._get_max_lens(news["description"])}\nназвание статьи: {news["title"]}'
            for news in self.news_json[:10]
        ]
        top_ten = "\n\n".join(top_ten)
        return f'в новостях топ 10 по длинне слов: {top_ten}'


if __name__ == '__main__':
    json_obj = MyParser()
    json_obj.parse_json('newsafr.json')
    print(json_obj.top_ten_json())