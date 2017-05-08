from pprint import pprint

words = ["banana", "pear", "apple", "lemon", "orange", "apricot", "pineapple", "grapes", "mishmish"]

def get_reversed(s):
    return s[::-1]


pprint(sorted(words, key=lambda s:s[::-1]))
print("-----------------------------")
pprint(sorted(words))

