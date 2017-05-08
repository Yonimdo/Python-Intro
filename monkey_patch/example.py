import time


def calculate_life():
    time.sleep(0.5)
    return 42


result = []
old = calculate_life


# type of lazy caching
#
# def calculate_life():
#     if not result:
#         result.append(old())
#     return result[0]



def get_stuff():
    time.sleep(2)
    return ['apple', 'pear']


def make_it_self_cache(f):
    result = []

    def new_f():
        if not result:
            result.append(f())
        return result[0]

    return new_f

@make_it_self_cache # == get_other_stuff = make_it_self_cache(make_it_self_cache)
def get_other_stuff():
    time.sleep(2)
    return ['apple', 'pear']





calculate_life = make_it_self_cache(calculate_life)
get_stuff = make_it_self_cache(get_stuff)

for x in range(10):
    print(calculate_life())
    print(get_stuff())
