from random import choice, seed


class CookBook:
    def __init__(self) -> None:
        self.book = {}

    @staticmethod
    def _parser(raw_lst: list[list]) -> list[dict]:
        """
        raw_lst: список с сырыми данными
        return: список словарей вида [{
            'ingredient_name': ingredient_name,
            'quantity': quantity,
            'measure': measure,}, {...}]
        """
        list_ingtidients = []
        for row in raw_lst:
            ingredient_name, quantity, measure = row.split(' | ')
            list_ingtidients.append({
                'ingredient_name': ingredient_name,
                'quantity': int(quantity),
                'measure': measure,
            })
        return list_ingtidients

    def read(self, path: str) -> None:
        """открывает файл на чтение рецепта и записывает к себе в словарь данные, где
        ключ: название блюда
        значение: рецепт блюда
        """
        with open(path, 'r', encoding='utf8') as file:
            for row in file.read().split('\n\n'):
                row = row.split('\n')
                head, body = row[0], row[2:]
                self.book[head] = self._parser(body)

    def help(self):
        if keys := '\n'.join(map(str, self.book)):
            return (f'Я знаю рецепты для:\n{", ".join(map(str, self.book))}\n'
                    f'например для просмотра рецепта для омлета \n'
                    f'обратитесь к моему словарю book: \n'
                    f'book[\'омлет\']')
        return 'Я не знаю ниодного рецепта'

    def get_shop_list_by_dishes(self, list_dishes: list, person_count: int = 1) -> dict[dict]:
        all_products = {}
        for dish in list_dishes:
            for ingr_s in self.book[dish]:
                if ingr_s['ingredient_name'] in all_products:
                    all_products[ingr_s['ingredient_name']
                                 ]['quantity'] += ingr_s['quantity'] * person_count
                else:
                    all_products[ingr_s['ingredient_name']] = {
                        'quantity': ingr_s['quantity'] * person_count,
                        'measure': ingr_s['measure'],
                    }
        return all_products

    def __str__(self) -> str:
        return str(self.book)

    __repr__ = __str__


if __name__ == '__main__':
    my_book = CookBook()
    my_book.read('res.txt')
    all_recipes = list(my_book.book)
    for elem in my_book.book['Запеченный картофель']:
        print(elem)
    print(my_book.get_shop_list_by_dishes(
        [choice(all_recipes) for _ in range(3)], 2))
    print(my_book.book)
