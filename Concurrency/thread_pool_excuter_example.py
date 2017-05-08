from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time, random


def func(number):
    print("func {} started".format(str(number)))
    wait = random.uniform(1, 10)
    time.sleep(wait)
    print("func {} ended after {} time".format(str(number), wait))


#
# with ThreadPoolExecutor(max_workers=4) as excuter:
#     for number in range(200):
#         excuter.submit(func, number)



if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as excuter:
        for number in range(200):
            excuter.submit(func, number)
print("done")
