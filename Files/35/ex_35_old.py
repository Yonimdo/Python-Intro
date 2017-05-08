

def parse_commands(filename):
    x, y = 0, 0
    # --- WRITE YOUR CODE HERE --- #
    infile = open(filename,"r");
    for line in infile:
        split = line.split(' ')
        if split[0] == "North":
            y += int(split[1])
        elif split[0] == "South":
            y -= int(split[1])
        elif split[0] == "East":
            x += int(split[1])
        elif split[0] == "West":
            x -= int(split[1])
    infile.close()
    # ---------------------------- #
    return x, y

result = parse_commands('journey_35.txt')
print("Result:", result)
assert (220, 180) == result

