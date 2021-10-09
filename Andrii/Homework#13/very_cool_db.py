from sqlalchemy import create_engine, Integer, Text, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from CONSTANTS import PSQL_USER, PSQL_PASSWORD, HOST
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from sqlalchemy.orm import relationship


engine = create_engine(f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{HOST}/cool_db1')
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    orders = relationship('Orders', backref='Customer')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float(10), nullable=False)

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime(),default=datetime.now())
    customer_id = Column(Integer, ForeignKey('customers.id'))
    paid = Column(Boolean, default=False)
    shipped = Column(Boolean, default=False)
    order_contents = relationship('Order_product', backref='Orders')

class Order_product(Base):
    __tablename__ = 'product_orders'
    order_id = Column(Integer, ForeignKey('orders.id'),primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)


class Discounts(Base):
    __tablename__ = 'discounts'
    order_id = Column(Integer, ForeignKey('orders.id'),primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    percents = Column(Integer, nullable=False )



if not database_exists(engine.url):
    create_database(engine.url)



Base.metadata.create_all(engine)