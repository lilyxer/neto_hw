import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, relationship
from environs import Env


def config() -> dict:
    """
    получаем данные для работы с базой данных
    """
    env = Env()
    env.read_env()
    return {
        'login': env('USER_DB'),
        'password': env('PASSWORD'),
        'db': env('DATABASE'),
        'my_db': env('CREATE_DB'),
        'host': env('HOST'),
        'port': env('PORT')
    }


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    """Создаёт класс-отношение для издателя
    id - уникальный номер
    name - имя издателя, строка, длина не более 50, уникально
    """
    __tablename__ = 'publisher'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=50), unique=True, nullable=False)

    def __str__(self):
        return f'издатель {self.id=}: {self.name,}'


class Book(Base):
    """Создаёт класс-отношение для книги
    id - уникальный номер
    title - название книги, строка, длина не более 150, уникально
    id_publisher - внешний ключ, ссылается на издателя
    """
    __tablename__ = 'book'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(length=150), nullable=False)
    id_publisher = sa.Column(sa.Integer,
                             sa.ForeignKey('publisher.id'),
                             nullable=False)

    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'книга {self.id=}: {self.title, self.id_publisher}'


class Shop(Base):
    """Создаёт класс-отношение для магазина
    id - уникальный номер
    name - название магазина, строка, длина не более 400, уникально
    """
    __tablename__ = 'shop'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=40), nullable=False)

    def __str__(self):
        return f'магазин {self.id=}: {self.name,}'


class Stock(Base):
    """Создаёт класс-отношение для связки книг с магазином
    id - уникальный номер
    id_book - внешний ключ, ссылается на книгу
    shop_id - внешний ключ, ссылается на магазин
    count - количество книг в магазине, целое число"""
    __tablename__ = 'stock'

    id = sa.Column(sa.Integer, primary_key=True)
    id_book = sa.Column(sa.Integer,
                        sa.ForeignKey('book.id'),
                        nullable=False)
    id_shop = sa.Column(sa.Integer,
                        sa.ForeignKey('shop.id'),
                        nullable=False)
    count = sa.Column(sa.Integer)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

    def __str__(self):
        return f'склад {self.id=}: {self.id_book, self.id_shop, self.count}'


class Sale(Base):
    """Создаёт класс-отношение покупки книги
    id - уникальный номер
    price - стоимость, вещественное число
    date_sale - дата продажи, тип date_time
    stock_id - внешний ключ, ссылается на склад
    count - количество заказанного, целое число"""
    __tablename__ = 'sale'

    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Float, nullable=False)
    date_sale = sa.Column(sa.DateTime, nullable=False)
    id_stock = sa.Column(sa.Integer,
                         sa.ForeignKey('stock.id'),
                         nullable=False)
    count = sa.Column(sa.Integer, nullable=False)
    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'продажа {self.id=}: {self.price, self.date_sale, self.id_stock, self.count}'


def create_tables(engine):
    """Создание, либо дроп отношений-классов
    engine - указатель на бд"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)