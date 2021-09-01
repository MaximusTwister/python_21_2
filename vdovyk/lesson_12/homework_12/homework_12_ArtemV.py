import random
from currency_list import currency_list
from faker import Faker
from datetime import datetime
from Luhn_algorithm import generator_card_number
import json

fkr = Faker()

class BankTransaction:
    transaction_data = dict.fromkeys(['transaction_id', 'amount', 'currency', 'description', 'receiver_card_owner',
                                      'receiver_card', 'card_owner', 'card', 'card_exp_month',
                                      'card_exp_year', 'card_cvv', 'transaction_time']
                                     )

    def __init__(self):
        self.transaction_id = self.transaction_id_func()
        self.amount = self.amount_func()
        self.currency = self.currency_func()
        self.description = self.description_func()
        self.receiver_card_owner = self.receiver_card_owner_func()
        self.receiver_card = self.receiver_card_func()
        self.card_owner = self.card_owner_func()
        self.card = self.card_func()
        self.card_exp_month = self.card_exp_month_func()
        self.card_exp_year = self.card_exp_year_func()
        self.card_cvv = self.card_cvv_func()
        self.transaction_time = self.transaction_time_func()
        self.file_json = self.json_func()

    def transaction_id_func(self):
        transaction_id = random.randint(1, 100000)
        self.transaction_data['transaction_id'] = transaction_id
        return transaction_id


    def amount_func(self):
        amount = random.randint(0, 1000000)/100
        self.transaction_data['amount'] = amount
        return amount

    def currency_func(self):
        currency = random.choice(currency_list)
        self.transaction_data['currency'] = currency
        return currency

    def description_func(self):
        description = f'order #{random.randint(1, 10000)}'
        self.transaction_data['description'] = description
        return description

    def receiver_card_owner_func(self):
        receiver_card_owner = fkr.name()
        self.transaction_data['receiver_card_owner'] = receiver_card_owner
        return receiver_card_owner

    def receiver_card_func(self):
        receiver_card = generator_card_number()
        self.transaction_data['receiver_card'] = receiver_card
        return receiver_card

    def card_owner_func(self):
        card_owner = fkr.name()
        self.transaction_data['card_owner'] = card_owner
        return card_owner

    def card_func(self):
        card = generator_card_number()
        self.transaction_data['card'] = card
        return card

    def card_exp_month_func(self):
        card_exp_month = random.randint(1, 12)
        self.transaction_data['card_exp_month'] = card_exp_month
        return card_exp_month

    def card_exp_year_func(self):
        year = int(datetime.today().strftime('%Y'))
        card_exp_year = random.randint(year+1, year+5)
        self.transaction_data['card_exp_year'] = card_exp_year
        return card_exp_year

    def card_cvv_func(self):
        card_cvv = str(random.randint(1, 999)).zfill(3)
        self.transaction_data['card_cvv'] = int(card_cvv)
        return int(card_cvv)

    def transaction_time_func(self):
        transaction_time = random.randint(1514757600, int(datetime.timestamp(datetime.now())))  # from 2018 year (in Unix time) to now
        self.transaction_data['transaction_time'] = str(datetime.fromtimestamp(transaction_time))
        return transaction_time

    def json_func(self):
        with open(f'bank_transaction #{self.transaction_id}.json', 'w') as json_file:
            json_str = json.dumps(self.transaction_data)
            file_json = json_file.write(json_str)

        return file_json


trans_1 = BankTransaction()
print(trans_1.transaction_data)


