import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    def __str__(self):
        return self.name


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=80), nullable=False)
    author_id = sq.Column(sq.Integer, sq.ForeignKey("author.id"), nullable=False)

    author = relationship(Author, backref="books")

    def __str__(self):
        return f"Название книги: {self.title}, Автор: {self.author}"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    def __str__(self):
        return f"Название магазина: {self.name}"

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)

    shop = relationship(Shop, backref="stocks")
    book = relationship(Book, backref="stocks")

    def __str__(self):
        return f"Книга: {self.book}, Магазин: {self.shop}, Количество: {self.count}"


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock = relationship(Stock, backref="sales")

    def __str__(self):
        return f"Книга: {self.stock.book}, Магазин: {self.shop}, Цена: {self.price}, Количество: {self.count}"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
