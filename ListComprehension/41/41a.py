def funny(s):
    lst = s.split()
    lst = [x[::-1].lower().title() for x in lst]
    # === YOUR CODE HERE! ===
    # =======================
    return " ".join(lst)

result = funny("Foo bar")
print(result)
assert result == "Oof Rab"

result = funny("The quick brown fox")
print(result)
assert result == "Eht Kciuq Nworb Xof"

print("OK") 