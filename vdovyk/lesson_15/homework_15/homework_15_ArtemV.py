from datetime import datetime
import random
from prettytable import PrettyTable

from constants import CATEGORY_OF_EXPENSES
from constants import ACCOUNTS
from constants import CATEGORY_OR_INCOME
from constants import DEFAULT_CURRENCY


class FinancialAccount:

    def __init__(self):
        self.__spending_list = list()
        self.__earnings_list = list()
        self.__account_info_list = list()
        self.__account_name = random.choice(ACCOUNTS)
        self.__balance = random.randint(1000, 10000000)/100

    def get_account(self):
        return {'account name': self.__account_name,
                'balance': self.__balance,
                'expenses': [str(el) for el in self.__spending_list],
                'incomes': [str(el) for el in self.__earnings_list]}

    def output_account_info(self):
        self.__account_info_list.append([self.get_account()['account name'],
                                         f'{self.get_account()["balance"]}{DEFAULT_CURRENCY}'])

        # Create pretty output
        x = PrettyTable()
        x.field_names = ['Account name', 'Balance']
        [x.add_row(file) for file in self.__account_info_list]
        return x

    def add_spending_item(self, purchase):
        self.__spending_list.append(purchase)
        return f'{purchase} added to {self.get_account()["account name"]}'

    def delete_spending_item(self, purchase):
        if purchase not in self.__spending_list:
            return {'status_code': 404, 'msg': 'Not Found in DB'}
        else:
            self.__spending_list.remove(purchase)
            return f'{purchase} deleted from {self.get_account()["account name"]}'

    def add_earnings_item(self, earnings):
        self.__earnings_list.append(earnings)
        return f'{earnings} added to account {self.get_account()["account name"]}'

    def delete_earnings_item(self, earnings):
        if earnings not in self.__earnings_list:
            return {'status_code': 404, 'msg': 'Not Found in DB'}
        else:
            self.__earnings_list.remove(earnings)
            return f'{earnings} deleted from account {self.get_account()["account name"]}'


class Expenses(FinancialAccount):

    def __init__(self):
        self.__purchase = dict()
        self.__create_purchase()

    def __str__(self):
        return f'{self.__purchase.get("name")}, cost: {self.__purchase.get("cost")}{DEFAULT_CURRENCY},'\
               f' at {self.__purchase.get("time")}'

    def __create_purchase(self):
        self.__purchase['name'] = random.choice(CATEGORY_OF_EXPENSES)
        self.__purchase['cost'] = random.randint(0, 100000)/100
        self.__purchase['time'] = str(datetime.now())

    def get_purchase_info(self):
        return self.__purchase

    def add_purchase(self):
        res = self.add_spending_item(self)
        print(f'Add result: {res}')

    def delete_purchase(self):
        res = self.delete_spending_item(self)
        print(f'Delete result: {res}')


class Income(FinancialAccount):

    def __init__(self):
        self.__earnings = dict()
        self.__create_income()

    def __str__(self):
        return f'{self.__earnings.get("name")}, earn: {self.__earnings.get("earn")}{DEFAULT_CURRENCY},'\

    def __create_income(self):
        self.__earnings['name'] = random.choice(CATEGORY_OR_INCOME)
        self.__earnings['earn'] = random.randint(0, 100000)/100

    def get_income_info(self):
        return self.__earnings

    def add_income(self):
        res = self.add_earnings_item(self.__earnings)
        print(f'Add result: {res}')

    def delete_income(self):
        res = self.delete_earnings_item(self.__earnings)
        print(f'Delete result: {res}')


def main():
    a_1 = FinancialAccount()
    a_2 = FinancialAccount()
    a_3 = FinancialAccount()

    e_1 = Expenses()
    e_2 = Expenses()
    e_3 = Expenses()
    e_4 = Expenses()
    e_5 = Expenses()
    e_6 = Expenses()
    e_7 = Expenses()
    e_8 = Expenses()
    e_9 = Expenses()

    i_1 = Income()
    i_2 = Income()
    i_3 = Income()
    i_4 = Income()

    print(a_1.add_spending_item(e_1))
    print(a_1.add_spending_item(e_2))
    print(f'{a_1.add_spending_item(e_3)}\n')

    print(a_2.add_spending_item(e_4))
    print(a_2.add_spending_item(e_5))
    print(f'{a_2.add_spending_item(e_6)}\n')

    print(a_3.add_spending_item(e_7))
    print(a_3.add_spending_item(e_8))
    print(f'{a_3.add_spending_item(e_9)}\n')

    print(a_1.add_earnings_item(i_1))
    print(a_1.add_earnings_item(i_2))
    print(f'{a_1.add_earnings_item(i_3)}\n')

    print(a_2.add_earnings_item(i_3))
    print(f'{a_2.add_earnings_item(i_4)}\n')

    print(f'{a_3.add_earnings_item(i_2)}\n')

    print(f'{a_1.get_account()}\n')
    print(f'{a_2.get_account()}\n')
    print(f'{a_3.get_account()}\n')

    print(a_1.output_account_info())
    print(a_2.output_account_info())
    print(a_3.output_account_info())


main()