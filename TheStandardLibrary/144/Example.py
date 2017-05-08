import sys
from pathlib import Path
from collections import defaultdict


if __name__ == '__main__':
    print("I am:", sys.argv[0])
    for i, s in enumerate(sys.argv[1:]):
        print("Parameter #{}: {}".format(i+1, s))



folder = Path('.')
for p in folder.iterdir():
    print(p, p.is_dir(), p.is_file(), p.stat().st_size, p.suffix)



def create_player():
    return {
        'hit points': 10,
        'money': 1000,
    }

players = defaultdict(create_player)

# defaultdict calls create_player on first access to players['foo'].
# There is no need to explicitly call:
#   players['foo'] = create_player()

players['Aragorn']['hit points'] += 5

players['Bilbo']['money'] += 50
players['Frodo']['hit points'] -= 1
for name, info in players.items():
    print(name, info)