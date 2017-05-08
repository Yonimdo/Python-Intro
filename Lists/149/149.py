data = [
    10,
    3,
    2,
    16,
    8,
    3,
    7,
    9,
    12,
    16,
    0,
    4,
    10,
]
mx = max(data)

for x in data:
    if x == mx:
        c = "*"
    else:
        c = "="
    print(c*x)
