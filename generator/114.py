def intputs(prompt=">> ", invalid_message="Invalid input"):
    """Generates a sequence of integers read from standard input, one per row,
    until an empty line is reached.  For non-numeric inputs, displays
    invalid_input to the users, and continues input.
    """
    # ----- YOUR CODE HE5RE! ----------------------
    while (True):
        user_input = input(prompt)
        try:
            if user_input == "":
                break
            yield int(user_input)
        except ValueError:
            print(invalid_message)


for x in intputs():
    print(x if x % 7 else "Boom!")
print("Done!")
