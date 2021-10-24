class Cash:
    _all_cash = {'Privat bank': 0.0, 'Raiffeisen': 0.0}
    _spending_categories = {'Restaurant and cafe': 0.0, 'alcohol': 0.0,
                            'utilities': 0.0, 'entertainments': 0.0, 'cigarettes': 0.0}
    _earnings_categories = {}

    @classmethod
    def up_cash(cls, cash, card):
        cls._all_cash.setdefault(card, 0.0)
        cls._all_cash[card] += cash

    @classmethod
    def add_earning_categories(cls, cash, earning_category):
        cls._earnings_categories.setdefault(earning_category, 0.0)
        cls._earnings_categories[earning_category] += cash

    @classmethod
    def income(cls, cash, card, earning_category):
        cls.up_cash(cash, card)
        cls.add_earning_categories(cash, earning_category)
        print(f'your card ({card}) was full on {cash} $ from {earning_category}, '
              f'now your balance is {cls._all_cash[card]} $')

    @classmethod
    def down_cash(cls, cash, card):
        if cls._all_cash.get(card, 0.0) > cash:
            cls._all_cash[card] -= cash
            return True
        else:
            print("you don't have enough money for trading transactions")
            return False

    @classmethod
    def apportioning_money(cls, cash, spending_category):
        cls._spending_categories.setdefault(spending_category, 0.0)
        cls._spending_categories[spending_category] += cash

    @classmethod
    def expenditure(cls, cash, card, spending_category):
        if cls.down_cash(cash, card):
            cls.apportioning_money(cash, spending_category)
            print(f'you spend {cash} from {card} on the {spending_category}')

    @classmethod
    def concatenation_spending_category(cls, name_for_new_category, *args):
        i = 0.0
        for category in args:
            cls._spending_categories.setdefault(category, 0.0)
            i += cls._spending_categories[category]
            del cls._spending_categories[category]
        cls._spending_categories.setdefault(name_for_new_category, 0)
        cls._spending_categories[name_for_new_category] += i

    @staticmethod
    def set_inform(dictionary):
        for el in dictionary:
            if dictionary[el]:
                print(f'{el}: {dictionary[el]}')

    @classmethod
    def my_income(cls):
        cls.set_inform(cls._earnings_categories)

    @classmethod
    def my_spend(cls):
        cls.set_inform(cls._spending_categories)

    @classmethod
    def my_balance(cls):
        cls.set_inform(cls._all_cash)

    @classmethod
    def clear_cash(cls):
        cls._all_cash.clear()

    @classmethod
    def clear_spending_categories(cls):
        cls._spending_categories.clear()

    @classmethod
    def clear_earning_categories(cls):
        cls._earnings_categories.clear()

    @classmethod
    def clear_all(cls):
        cls.clear_cash()
        cls.clear_spending_categories()
        cls.clear_earning_categories()
        print('all clear')
