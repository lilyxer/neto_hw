import requests
from environs import Env

def config(token_name: str) -> str:
    env = Env()
    env.read_env()
    return env(token_name)

class MyTranslator:
    URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

    def __init__(self, key: str, text: str, lang: str = 'ru-en') -> None:
        self.key = key
        self.text = text
        self.lang = lang
        self._dict = {}

    def _f(self):
        params = {'key': self.key,
                  'text': self.text,
                  'lang': self.lang,}
        resp = requests.get(url=self.URL, params=params)
        word = resp.json()['def'][0].get('tr', [])[0].get('text', '')
        self._dict['text'] = word
        return word

    def __str__(self) -> str:
        return self._dict.get(self.text) or self._f()

def translate_word(word):
    token = config('ya_token_translate')
    return MyTranslator(key=token, text=word)



if __name__ == '__main__':
    token = config('ya_token_translate')
    text = 'машина'
    translate = MyTranslator(key=token, text=text)
    print(translate)
