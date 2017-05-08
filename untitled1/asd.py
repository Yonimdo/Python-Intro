s = "foo bar"

target = []
for x in s.split():
    target.append(x[::-1].title())
print(' '.join(target))
