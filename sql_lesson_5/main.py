import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from classes import *
from create_db import create_database
from dump_json import *


# Подключаемся к постгрес, создаем движок
# Data Source Name
# необходимо прописать вашу БД и данные для подключения
_config = config()
DSN = f"postgresql://{_config['login']}:{_config['password']}@{_config['host']}:{_config['port']}/{_config['db']}"
engine = sa.create_engine(DSN)

create_database(_config)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

def drop_to_bd(my_dict: dict) -> None:
    """Принимает словарь, добавляем записи в классы
    my_dict - словарь с данными из json
    """
    for record in my_dict:
        model = {
                 'publisher': Publisher,
                 'shop': Shop,
                 'book': Book,
                 'stock': Stock,
                 'sale': Sale,}[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

def select_shop(session) -> str:
    """
    Выводит название магазинов (shop), в которых представлены
    книги конкретного издателя и есть в наличии
    SELECT DISTINCT(shop.name)
    FROM shop
    INNER JOIN stock ON shop.id = stock.id_shop
    INNER JOIN book ON book.id = stock.id_book
    WHERE book.id_publisher = (
        SELECT publisher.id
        FROM publisher
        WHERE publisher.name = '%s') AND stock.count > 0;
    """
    publ = '4' #input('введите название или id издателя ')

    if publ.isdigit():
        subq = session.query(Publisher).filter(Publisher.id == int(publ)).subquery()
        publ = session.query(Publisher).filter(Publisher.id == int(publ)).all()

    else:
        subq = session.query(Publisher).filter(Publisher.name == publ).subquery()
        publ = session.query(Publisher).filter(Publisher.name == publ).all()

    if publ:
        publ = publ[0]
        if (
            response_query := session.query(Shop)
            .join(Stock)
            .join(Book)
            .join(subq, Book.id_publisher == subq.c.id)
            .filter(Stock.count > 0)
            .all()
        ):
            response_query = ', '.join([str(r) for r in response_query])
            return f'{publ} найден в {response_query}'

    return 'издатель в магазинах не найден'

# скачиваем json
URL = 'https://raw.githubusercontent.com/netology-code/py-homeworks-db/SQLPY-76/06-orm/fixtures/tests_data.json'
if answer := get_file(URL):
    drop_to_bd(answer)

# выборка магазина
print(select_shop(session))

session.close()