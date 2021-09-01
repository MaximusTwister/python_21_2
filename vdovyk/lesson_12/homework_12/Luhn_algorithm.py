import random

def luna(card_num):
    even_num = card_num[::2]
    sum_odd_num = sum(int(el) for el in list(card_num[1::2]))

    sum_ = sum(((int(el) * 2) // 10 + (int(el) * 2) % 10) for el in even_num)

    return (sum_odd_num + sum_) % 10

def generator_card_number():
    result = str(random.randint(3, 5))
    for i in range(2, 16):
        random.seed()
        result += str(random.randint(1, 9))
        
    for i in range(0, 9):
        if luna(result + str(i)) == 0:
            result += str(i)
            return result
