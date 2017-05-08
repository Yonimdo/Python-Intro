
def rotate(str):
    """ Returns the last char in str and puts it in the start of the string
    :param str: a string to be
    """
    return str[-1] + str[0:-1]

result = rotate("abcd")
print(result)
assert "dabc" == result
assert "hello world" == rotate("ello worldh")
assert "x" == rotate("x")
