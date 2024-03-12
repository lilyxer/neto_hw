import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from classes import *
from create_db import create_database
from dump_json import *


# Подключаемся к постгрес, создаем движок
# Data Source Name
# необходимо прописать вашу БД и данные для подключения
_config = config()
DSN = f"postgresql://{_config['login']}:{_config['password']}@{_config['host']}:{_config['port']}/{_config['my_db']}"
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
    принимает имя или идентификатор издателя (publisher)
    Выводит построчно факты покупки книг этого издателя
    """
    publ = '3'

    subq = (session.query(Publisher).filter(Publisher.id == int(publ)).subquery()
            if publ.isdigit() else
            session.query(Publisher).filter(Publisher.name == publ).subquery())

    if (response_query := session.query(Book.title, Shop.name,
                                        Sale.price * Sale.count, Sale.date_sale)
                                        .select_from(Shop)
                                        .join(Stock)
                                        .join(Book)
                                        .join(Sale)
                                        .join(subq, Book.id_publisher == subq.c.id)
                                        .filter(Stock.count > 0)
                                        .all()):
        for book, publisher, total, dt in response_query:
            print(f"{book: <40} | {publisher: <10} | {total: <8} | {datetime.strftime(dt, '%d-%m-%Y')}")

    return 'издатель в магазинах не найден'

# скачиваем json
URL = 'https://raw.githubusercontent.com/netology-code/py-homeworks-db/SQLPY-76/06-orm/fixtures/tests_data.json'
if answer := get_file(URL):
    drop_to_bd(answer)

# выборка магазина
select_shop(session)

session.close()