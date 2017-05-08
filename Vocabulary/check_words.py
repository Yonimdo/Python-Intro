from collections import Counter


def check_words(filename, tests):
    results = Counter({k: 0 for k in tests})
    with open(filename) as f:
        for line in f:
            s = line.strip()
            for name, test in tests.items():
                if test(s):
                    results[name] += 1
    return results


tests = {
    "Words with more than 3 letters": lambda w: len(w) > 3,
    "Word starts with a vowel:": lambda w: len(w)>1 and w[0] in "aeiou",
    "Word ends with a vowel:": lambda w: w[-1] in "aeiou",
    "Word ends with a vowel:": lambda w: True,
    "All words:": lambda w: True,
    "Word has only vowels:": lambda w: all([x in "aeiou" for x in w]),
    "Word does not have any vowel:": lambda w: all([x not in "aeiou" for x in w]),
    "Word starts and ends with the same letter:": lambda w: len(w) > 2 and w[0] == w[-1],
    "Word is a palindrome:": lambda w: len(w) > 2 and w[::-1] == w,
    "Word has two identical letters consecutively": lambda w: len(w) > 2 and any([v == w[k + 1] for k, v in enumerate(w[:-1])]),
    "Word has three identical letters consecutively": lambda w: len(w) > 2 and any([v == w[k + 1] == w[k + 2] for k, v in enumerate(w[:-2])]),

    # TODO
}

results = check_words('wordsEn.txt', tests)
for k, v in results.items():
    print(k, v)
