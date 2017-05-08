def outer():
    def inner(text):
        print(n)
        print(text)

    n = 100
    return inner


f = outer()
f("text")


def partial(f, *args):
    def new_f(*more_args):
        return f(*args, *more_args)
    return new_f

def foo(a,b,c,d,e,f,g):
    pass


foo(1, 2, 3, 4, 5, 6, "yoni")
foo(1, 2, 3, 4, 5, 6, "david")
foo(1, 2, 3, 4, 5, 6, "tohar")
foo(1, 2, 3, 4, 5, 6, "yuval")
foo(1, 2, 3, 4, 5, 6, "yoni")

better_foo = partial(foo, 1, 2, 3, 4, 5, 6)
# more_args
better_foo("yoni")
better_foo("david")
better_foo("tohar")
better_foo("yuval")
better_foo("yoni")
