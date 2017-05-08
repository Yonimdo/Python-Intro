def funny(s):
    target = []
    target = [x[::-1].title() for x in s.split()]
    #    for x in s.split():
    #        target.append(x[::-1].title())

    return ' '.join(target)

        # =======================


result = funny("Foo bar")
print(result)
assert result == "Oof Rab"

result = funny("The quick brown fox")
print(result)
assert result == "Eht Kciuq Nworb Xof"

print("OK")
def g(s):
    return s[0] in 'AEIOU'
