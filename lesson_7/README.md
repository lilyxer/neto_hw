## Задание 1
- спарсить текстовый файл с рецептом в словарь вида
```python
cook_book = {
  'Омлет': [
    {'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
    {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
    {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
    ], ...}
```

## Задание 2
- реализовать метод который принимает в себя название блюда и количество персон
- возвращает словарь со всеми ингридиентами и суммированной массой

## Задание 3
- просканировать папку в которой какой то количество текстовых файлов
- создать новый текстовый файл в который записать все найденные файлы отсортировав их по количеству строк
- оформить в виде:
```
2.txt
1
Строка номер 1 файла номер 2
1.txt
2
Строка номер 1 файла номер 1
Строка номер 2 файла номер 1
```
