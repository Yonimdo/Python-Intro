import functools
# see functools for build_in  decorators

def my_decorator(f):
    @functools.wraps(f)
    def df(*arg):
        print("BEFORE")
        ret =f(*arg)
        print("AFTER")
        return ret
    return df

@my_decorator
def greet(name):
    print("hello "+name)

greet("yoni")

