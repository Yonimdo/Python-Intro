max_input = 100
print("Choose a secret number between 1 and ", max_input)
current_delta = max_input / 2
computer_guess = current_delta

while True:
    print("Is your number {}?(y ,n)".format(computer_guess), computer_guess)
    if input().capitalize() == "y".capitalize():
        break
    else:
        current_delta /= 2
        print("Is my guess higher than the secret number? (y ,n)")
        if input().capitalize() == "y".capitalize():
            current_delta /= 2
            computer_guess -= current_delta
        else:
            current_delta /= 2
            computer_guess += current_delta
