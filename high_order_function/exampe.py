def call_twice(f, args=[], kwargs={}):
    f(*args, **kwargs)
    f(*args, **kwargs)


def fun(n=""):
    print(n)


call_twice(fun)

call_twice(fun, kwargs={"n": "yoni"})
call_twice(fun, args=['args'])
