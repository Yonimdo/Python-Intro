def count(num=0):
    try:
        count(num + 1)
    except RecursionError:
        print("Max Call stack:  {}".format(num))


count()
