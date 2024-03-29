import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Publisher: {self.id}, {self.name}'


class book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(publisher, backref="book")

    def __str__(self):
        return f'{self.title}'

class shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    
    def __str__(self):
        return f'{self.name}'

class stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(book, backref="stock")
    shop = relationship(shop, backref="stock")

    def __str__(self):
        return f'{self.count}'

class sale(Base):
     __tablename__ = 'sale'

     id = sq.Column(sq.Integer, primary_key=True)
     price = sq.Column(sq.Float)
     date_sale = sq.Column(sq.Date)
     stoсk_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
     count = sq.Column(sq.Integer)

     stock = relationship(stock, backref="sale")

     def __str__(self):
        return f' {self.date_sale}'


def create_tables(engine):
     Base.metadata.drop_all(engine)
     Base.metadata.create_all(engine)
     



