def emphasize(s):
    return "***{}***".format(s).upper()


print(type(emphasize))

def get_life():
    return 42

print(type(get_life))


print(emphasize("Hello!"))

em = emphasize

print(em("good morning"))

emphasize = get_life

print(emphasize())

del get_life

# get_life() # ==> NameError

print(em("hello"))
print(emphasize())

del em

# em("foo") # ==> NameError

emphasize = 17

print(emphasize)
print(type(emphasize))