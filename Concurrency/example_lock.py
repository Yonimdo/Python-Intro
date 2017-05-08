import threading

x = 0
x_lock = threading.Lock()


def add_one():
    global x
    for i in range(100000):
        with x_lock:
            x += 1
        #x_lock.release()


def remove_one():
    global x
    for i in range(100000):
        x_lock.acquire()
        x -= 1
        x_lock.release()


add = threading.Thread(target=add_one)
add.start()
remove = threading.Thread(target=remove_one)
remove.start()

for thrd in [add, remove]:
    thrd.join()

print(x)
