import os

import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from Models import create_tables, publisher, book, shop, stock, sale

def filling_and_connection():
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
             pb = publisher(name =i['fields']['name'])
             session.add(pb)
         elif i['model'] == 'book':
             bk = book(title =i['fields']['title'],publisher_id=i['fields']['id_publisher'])
             session.add(bk)
         elif i['model'] == 'shop':
             sh = shop(name =i['fields']['name'])
             session.add(sh)
         elif i['model'] == 'stock':
             st = stock(book_id=i['fields']['id_book'],shop_id=i['fields']['id_shop'],count=i['fields']['count'])
             session.add(st)
         elif i['model'] == 'sale':
             sa = sale(price=float(i['fields']['price']),date_sale=i['fields']['date_sale'],count=i['fields']['count'], stoсk_id =i['fields']['id_stock'])
             session.add(sa)  
  session.commit()
  return session


def get_shops(session, publisher_param): 
    subs= session.query( 
        book.title, shop.name, sale.price, sale.count, sale.date_sale
        ).select_from(shop).join(stock).join(book).join(publisher).join(sale) 
    if publisher_param.isdigit(): 
        result = subs.filter(publisher.id == publisher_param).all() 
    else:
        result = subs.filter(publisher.name == publisher_param).all() 
    for book_title, shop_name, price, count, date_sale in result: 
        revenue = price*count
        print(f"{book_title: <40} | {shop_name: <10} | {revenue: <8} | {date_sale.strftime('%d-%m-%Y')}") 
    session.close


if __name__ == '__main__':
    publisher_param = input('Введите название издательства: ') 
    get_shops(filling_and_connection(),publisher_param) 

    



