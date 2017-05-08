def sum_of_pairs(numbers):
    result = []
    for i in range(0, (len(numbers) - 1)):
        result.append(numbers[i] + numbers[i + 1])
    return result


assert sum_of_pairs([10, 5, 3, 20, 9, 1, 100, 7]) == [15, 8, 23, 29, 10, 101, 107]
assert sum_of_pairs([3, 7]) == [10]
assert sum_of_pairs([1, 1, 1]) == [2, 2]
assert sum_of_pairs(sum_of_pairs([1, 1, 1])) == [4]
