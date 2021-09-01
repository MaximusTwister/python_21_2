import random

def luna(card_num):
    even_num = card_num[::2]
    odd_num = list(card_num[1::2])
    sum_odd_num = 0

    for i in odd_num:
        sum_odd_num += int(i)

    sum_ = 0

    for i in even_num:
        tmp_num = int(i) * 2
        sum_ += tmp_num // 10 + tmp_num % 10

    return (sum_odd_num + sum_)%10

def generator_card_number():
    result = str(random.randint(3, 5))
    for i in range(2, 16):
        random.seed()
        result += str(random.randint(1, 9))
        
    for i in range(0, 9):
        if luna(result + str(i)) == 0:
            result += str(i)
            return result
