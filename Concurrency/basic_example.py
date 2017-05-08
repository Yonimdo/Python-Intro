import random,time,threading

def threading_func(number):
    time.sleep(random.uniform(0,5))
    print("Exiting thread #"+str(number))

def working():
    while True:
        time.sleep(0.5)
        print("Tick!")
        time.sleep(0.5)
        print("Tock!")

threads = []
for i in range(1,11):
    print("Starting thread #"+str(i))
    current = threading.Thread(target=threading_func, args=(i,))
    current.start()
    threads.append(current)
    print("i")

current = threading.Thread(target=working)
current.setDaemon(True)
current.start()

for thrd in threads:
    thrd.join()

print("Done!")