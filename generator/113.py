def accumulate(data):
    total = 0
    for x in data:
        total += x
        yield x, total


for i, total in accumulate(range(1, 11)):  # in python 2: use xrange.
    print(i, total)

print()

for i, total in accumulate([100, 10, 5, 200]):
    print(i, total)
