import urllib

from concurrent import futures


def load_url(url):
    return urllib.urlopen(url).read()


with futures.ThreadPoolExecutor(max_workers=3) as executor:
    f1 = executor.submit(load_url, 'http://www.foxnews.com/')
    f2 = executor.submit(load_url, 'http://www.ynet.co.il/')
    f3 = executor.submit(load_url, 'http://www.nrg.co.il/')
    f4 = executor.submit(load_url, 'http://www.walla.co.il/')
    f5 = executor.submit(load_url, 'http://www.yahoo.com/')

    print(f1, f1.running(), f1.done())
    print(f2)
    print(f3)
    print(f4)
    print(f5, f5.running(), f5.done())

    print("DONE (1)")

print("DONE (2)")

print(f1, f1.running(), f1.done())
print(f2)
print(f3)
print(f4)
print(f5, f5.running(), f5.done())
