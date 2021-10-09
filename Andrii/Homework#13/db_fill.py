import random

from very_cool_db import engine, Customer, Product, Orders, Order_product
from CONSTANTS import BRANDS, COLORS, GOODS

from random import choice
from faker import Faker
from sqlalchemy.orm import sessionmaker


session = sessionmaker(bind=engine)()
fkr = Faker()

def create_customer(customers_count=1):
    for i in range(customers_count):
        name = fkr.name()
        email = fkr.email()
        phone = fkr.msisdn()
        customer = Customer(customer_name=name, email=email, phone=phone)
        save_to_db(customer)

def create_product(product_count=1):
    for i in range(product_count):
        name = choice(GOODS)
        desq = f'{choice(BRANDS)},{choice(COLORS)},{name}'
        price = round(random.uniform(10, 900), 2)
        product = Product(product_name=name, description=desq, price=price)
        save_to_db(product)



def save_to_db(obj):
    session.add(obj)
    session.commit()

def main():
    create_customer(10)
    create_product(20)
    c1 = create_customer()
    c2 = create_customer()
    c3 = create_customer()
    i1 = create_product()
    i2 = create_product()
    i3 = create_product()

    o1 = Orders(Customer=c1)
    o2 = Orders(Customer=c2)
    item1 = Order_product(Orders=o1, product_id=i3, quantity=3)
    item2 = Order_product(Orders=o2, product_id=i2, quantity=5)
    save_to_db(o1)
    save_to_db(o2)

main()