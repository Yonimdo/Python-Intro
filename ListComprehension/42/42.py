def word_lengths(s):
    # ==== YOUR CODE HERE ===
    # =======================
    return [len(w) for w in s.split()]

def max_word_length(s):
    # ==== YOUR CODE HERE ===
    # =======================
    return max(word_lengths(s))

result = word_lengths("Contrary to popular belief Lorem Ipsum is not simply random text")
print("Result:", result)
assert result == [8, 2, 7, 6, 5, 5, 2, 3, 6, 6, 4]
print("OK")

result = max_word_length("Contrary to popular belief Lorem Ipsum is not simply random text")
print("Result:", result)
assert result == 8
print("OK")


