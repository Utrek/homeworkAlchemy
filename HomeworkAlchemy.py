import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from Models import create_tables, Publisher, Book, Shop, Stock, Sale
import json
import os

login = os.getenv('login')
password = os.getenv('password')
bd_name = os.getenv('Bd_name')

DSN = f'postgresql://{login}:{password}@localhost:5432/{bd_name}'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

path = 'tests_data.json'

Session = sessionmaker(bind=engine)
session = Session()

with open(path,'r') as f:
    data = json.loads(f.read())
    
    for i in data:
         if i['model'] == 'publisher':
             pb = Publisher(name =i['fields']['name'])
             session.add(pb)
         elif i['model'] == 'book':
             bk = Book(title =i['fields']['title'],publisher_id=i['fields']['id_publisher'])
             session.add(bk)
         elif i['model'] == 'shop':
             sh = Shop(name =i['fields']['name'])
             session.add(sh)
         elif i['model'] == 'stock':
             st = Stock(book_id=i['fields']['id_book'],shop_id=i['fields']['id_shop'],count=i['fields']['count'])
             session.add(st)
         elif i['model'] == 'sale':
             sa = Sale(price=float(i['fields']['price']),date_sale=i['fields']['date_sale'],count=i['fields']['count'], stoсk_id =i['fields']['id_stock'])
             session.add(sa)  
session.commit()

publisher_name = input('Введите название издательства: ')

subq = session.query(Publisher).join(Book.publisher).filter(Publisher.name == publisher_name).subquery()
for book_title in session.query(Book).join(subq, Book.publisher_id == subq.c.id).all():
   for i in session.query(Book).join(Stock.book).filter(Book.id== book_title.id).all():
       for c in session.query(Stock).filter(Stock.book_id ==i.id).all():
           for shop_name in session.query(Shop).join(Stock.shop).filter(Stock.id == c.id).all():
               for p in session.query(Stock).join(Sale.stock).filter(Stock.id == c.id).all():
                  for date_sale in session.query(Sale).filter(Sale.stoсk_id == p.id):
                      revenue = date_sale.count*date_sale.price
                      print (f'{book_title} |{shop_name} |{revenue}|{date_sale}')

session.close


    



