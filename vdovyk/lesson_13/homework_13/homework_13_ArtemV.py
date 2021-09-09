import random
import uuid

from customer_list import customer_list
from item_list import items


def autorization():
    autorization = random.randint(0, 1)  # 0 - not authorized; 1 - authorized
    if autorization == 1:
        customer_info = random.choice(customer_list)
    else:
        customer_info = dict.fromkeys(['customer_id', 'name', 'shipping_address',
                                       'payment_card', 'spent_total_amount', 'orders_list'])
        customer_info['customer_id'] = uuid.uuid4().hex[:6]
        customer_info['spent_total_amount'] = 0
        customer_info['orders_list'] = []

    return customer_info


current_customer = autorization()


class Customer:

    def __init__(self):
        self.customer_info = self.get_customer_info()

    def get_customer_info(self):
        customer_info = current_customer
        return customer_info


class Items:

    def __init__(self):
        super().__init__()
        self.item_info = self.get_item()

    def get_item(self):
        item_info = items
        return item_info


class PersonalDiscount(Customer):

    def __init__(self):
        super().__init__()
        self.discount_value = self.calc_discount_value()

    def calc_discount_value(self):
        if self.customer_info['spent_total_amount'] >= 10000:
            discount_value = 0.8                                       # Discount value = 20%
        elif 5000 <= self.customer_info['spent_total_amount'] < 10000:
            discount_value = 0.9                                       # Discount value = 10%
        elif 1000 <= self.customer_info['spent_total_amount'] < 5000:
            discount_value = 0.95                                      # Discount value = 5%
        else:
            discount_value = 1.0                                       # Discount value = 0%

        return discount_value


class Order(Items, PersonalDiscount):

    def __init__(self):
        super().__init__()
        self.order_list = self.get_order_list()

    def get_order_list(self, order_cost=0):
        self.number_of_items = random.randint(1, 10)
        order = dict.fromkeys(['order_list', 'order_cost', 'order_cost_with_discount', 'discount_value'])
        order_list = list()
        discount = self.discount_value

        for _ in range(self.number_of_items):
            item_tmp = random.choice(self.item_info)
            order_list.append(item_tmp)
            order_cost += item_tmp['cost']

        self.customer_info['spent_total_amount'] += order_cost * discount
        self.customer_info['orders_list'] += order_list
        order['order_list'] = order_list
        order['order_cost'] = order_cost
        order['order_cost_with_discount'] = round((order_cost * discount), 2)
        order['discount_value'] = f'{100 - (discount * 100)}%'
        return order


customer_1 = Customer()
print(f'Information about customer before adding items to shopping cart:\n{customer_1.customer_info}\n')

order_1 = Order()
print(f"Customer's order list:\n{order_1.order_list}\n")
print(f'Information about customer after adding items to shopping cart:\n{order_1.customer_info}\n')






