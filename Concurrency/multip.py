import multiprocessing


def print_one():
    for i in range(100000):
        print(1)


def print_negative_one():
    for i in range(100000):
        print(-1)


add = multiprocessing.Process(target=print_one)

remove = multiprocessing.Process(target=print_negative_one)

if __name__ == '__main__':
    add.start()
    remove.start()
