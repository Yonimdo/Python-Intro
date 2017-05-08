def count_number_sum(number):
    sum = 0
    while (number > 0):
        current_digit = number % 10
        sum += current_digit
        number = number // 10
    return sum


def check_number(number):
    sum = count_number_sum(number)
    number_true = number % 7 == 0
    sum_true = sum % 7 == 0
    if number_true and sum_true:
        return number, sum
    elif number_true:
        return 'boom!', sum
    elif sum_true:
        return number, 'boom!'
    return number, sum


for number in range(1, 100):
    print("{} {}".format(*check_number(number)))
