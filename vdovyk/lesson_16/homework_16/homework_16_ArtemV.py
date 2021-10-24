import os
import random

import psycopg2
from psycopg2 import sql
from faker import Faker

from constants import NAME_OF_PRODUCT
from constants import PRODUCT_DESCRIPTION

db_name = input('Please, enter Database name')
db_user = os.environ['USER']
db_password = 'fdedfSEDAf'
db_host = 'localhost'


# Create tables
def create_table_customers():
    with psycopg2.connect(dbname=db_name,
                          user=db_user,
                          password=db_password,
                          host=db_host) as conn:
        with conn.cursor() as cursor:
            cursor.execute('CREATE EXTENSION CITEXT')
            cursor.execute('CREATE TABLE customers'
                           '(customer_id serial primary key,'
                           'customer_name varchar(100) NOT NULL,'
                           'email CITEXT NOT NULL,'
                           'phone varchar(100) NOT NULL)')

    print('Table "customers" created')


def create_table_product():
    with psycopg2.connect(dbname=db_name,
                          user=db_user,
                          password=db_password,
                          host=db_host) as conn:
        with conn.cursor() as cursor:
            cursor.execute('CREATE TABLE product'
                           '(product_id serial primary key,'
                           'product_name varchar(100),'
                           'description text,'
                           'price INTEGER DEFAULT 0.0)')

    print('Table "product" created')


def create_table_orders():
    with psycopg2.connect(dbname=db_name,
                          user=db_user,
                          password=db_password,
                          host=db_host) as conn:
        with conn.cursor() as cursor:
            cursor.execute('CREATE TABLE orders'
                           '(order_id serial primary key,'
                           'order_date TIMESTAMP NOT NULL DEFAULT NOW(),'
                           'customer_id INTEGER REFERENCES customers(customer_id) on delete RESTRICT,'
                           'paid BOOLEAN NOT NULL DEFAULT FALSE,'
                           'shipped BOOLEAN NOT NULL DEFAULT FALSE)')

    print('Table "orders" created')


def create_table_order_product():
    with psycopg2.connect(dbname=db_name,
                          user=db_user,
                          password=db_password,
                          host=db_host) as conn:
        with conn.cursor() as cursor:
            cursor.execute('CREATE TABLE order_product'
                           '(order_id INTEGER REFERENCES orders(order_id) on delete CASCADE,'
                           'product_id INTEGER REFERENCES product(product_id) on delete SET NULL)')

    print('Table "order_product" created')


def create_table_discount():
    with psycopg2.connect(dbname=db_name,
                          user=db_user,
                          password=db_password,
                          host=db_host) as conn:
        with conn.cursor() as cursor:
            cursor.execute('CREATE TABLE discount'
                           '(order_id INTEGER REFERENCES orders(order_id) on delete CASCADE,'
                           'product_id INTEGER REFERENCES product(product_id) on delete SET NULL,'
                           'percents INTEGER NOT NULL)')

    print('Table "discount" created')


# Fill the tables

def create_user():
    fkr = Faker()

    with psycopg2.connect(dbname=db_name,
                          user=db_user,
                          password=db_password,
                          host=db_host) as conn:
        with conn.cursor() as cursor:
            user_name = fkr.name()
            user_email = fkr.email()
            user_phone = fkr.phone_number()

            # INSERT INTO customers (customer_name, email, phone)
            query = sql.SQL('insert into {0}({1}) values (%s, %s, %s)').format(
                sql.Identifier('customers'),
                sql.SQL(', ').join([sql.Identifier('customer_name'),
                                    sql.Identifier('email'),
                                    sql.Identifier('phone'),
                                    ]))

            cursor.execute(query.as_string(conn), [user_name, user_email, user_phone])

            print(f'Customer: {user_name}, {user_email}, {user_phone} added to table "customers"')


def create_product():
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host) as conn:
        with conn.cursor() as cursor:
            product_name = random.choice(NAME_OF_PRODUCT)
            description = random.choice(PRODUCT_DESCRIPTION)
            price = random.randint(5, 300)

            query = sql.SQL('insert into {0}({1}) values (%s, %s, %s)').format(
                sql.Identifier('product'),
                sql.SQL(', ').join([sql.Identifier('product_name'),
                                    sql.Identifier('description'),
                                    sql.Identifier('price'),
                                    ]))

            cursor.execute(query.as_string(conn), [product_name, description, price])

            print(f'Product: {product_name}, {description}, {price}$ added to table "product"')


def create_orders(customer_id):
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host) as conn:
        with conn.cursor() as cursor:
            query = sql.SQL('insert into {0}({1}) values (%s)').format(
                sql.Identifier('orders'),
                sql.Identifier('customer_id'))

            cursor.execute(query.as_string(conn), [customer_id])

            print(f'Customer {customer_id} made an order')


def create_order_product(order_id):
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host) as conn:
        with conn.cursor() as cursor:
            for _ in range(random.randint(1, 10)):
                product_id = random.randint(1, 10)

                query = sql.SQL('insert into {0}({1}) values (%s, %s)').format(
                    sql.Identifier('order_product'),
                    sql.SQL(', ').join([sql.Identifier('order_id'),
                                        sql.Identifier('product_id'),
                                        ]))

                cursor.execute(query.as_string(conn), [order_id, product_id])

        print(f'Order_product added to table "order_product"')


# Enter point
def create_tables():
    create_table_customers()
    create_table_product()
    create_table_orders()
    create_table_order_product()
    create_table_discount()


def fill_the_tables():
    for i in range(1, 11):
        create_user()
    for i in range(1, 11):
        create_product()
    for i in range(1, 11):
        create_orders(i)
    for i in range(1, 11):
        create_order_product(i)


create_tables()
fill_the_tables()


