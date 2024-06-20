import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import *

with open("connect.json", encoding="utf-8") as file:
    data = json.load(file)
    name = data["name"]
    password = data["password"]
    host = data["host"]
    port = data["port"]
    db_name = data["db_name"]

DSN = f'postgresql://{name}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

# Создание таблиц и связей
create_tables(engine)

# Добавление данных
author1 = Author(id=1, name="Толстой")
author2 = Author(id=2, name="Гоголь")
author3 = Author(id=3, name="Лермонтов")
author4 = Author(id=4, name="Достоевский")
author5 = Author(id=5, name="Булгаков")

shop1 = Shop(id=1, name="Магазин 1")
shop2 = Shop(id=2, name="Магазин 2")
shop3 = Shop(id=3, name="Магазин 3")


book1 = Book(id=1, title="Война и мир", author=author1)
book2 = Book(id=2, title="Мцыри", author=author2)
book3 = Book(id=3, title="Три мушка", author=author3)
book4 = Book(id=4, title="Преступление и наказание", author=author4)
book5 = Book(id=5, title="Белая гвардия", author=author5)
book6 = Book(id=6, title="Идиот", author=author5)

stock1 = Stock(id=1, count=10, shop=shop1, book=book1)
stock2 = Stock(id=2, count=15, shop=shop2, book=book2)
stock3 = Stock(id=3, count=20, shop=shop3, book=book3)
stock4 = Stock(id=4, count=25, shop=shop1, book=book4)
stock5 = Stock(id=5, count=30, shop=shop2, book=book5)
stock6 = Stock(id=6, count=35, shop=shop3, book=book6)

sale1 = Sale(id=1, price=1000, date_sale="2022-01-01", count=1, stock=stock1)
sale2 = Sale(id=2, price=2000, date_sale="2022-02-01", count=2, stock=stock2)
sale3 = Sale(id=3, price=3000, date_sale="2022-03-01", count=3, stock=stock3)
sale4 = Sale(id=4, price=4000, date_sale="2022-04-01", count=4, stock=stock1)
sale5 = Sale(id=5, price=5000, date_sale="2022-05-01", count=5, stock=stock2)
sale6 = Sale(id=6, price=6000, date_sale="2022-06-01", count=6, stock=stock3)


session.add_all([author1, author2, author3, author4, author5])
session.add_all([shop1, shop2, shop3])
session.add_all([book1, book2, book3, book4, book5, book6])
session.add_all([stock1, stock2, stock3, stock4, stock5, stock6])
session.add_all([sale1, sale2, sale3, sale4, sale5, sale6])
session.commit()

query = input('Введи фамилию автора или его id: ')
for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Stock, Book.id == Stock.book_id)\
        .join(Shop, Stock.shop_id == Shop.id)\
        .join(Sale, Stock.id == Sale.stock_id)\
        .join(Author, Book.author_id == Author.id)\
        .filter(Author.name == query or Author.id == query).all():
    print(f"{c[0]} | {c[1]} | {c[2]} | {c[3]}")

session.close()
