def nachmannize(s):
    space = " "
    result = []
    for k, v in enumerate(s):
        result.append(s[:k + 1])
    return space.join(result) 

print(nachmannize("abcd"))

# assert nachmannize("abcd") == "a ab abc abcd"
