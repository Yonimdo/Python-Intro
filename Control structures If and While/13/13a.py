correct = False
correct_text = "Your guess is correct!"
wrong_text = "Player two,{}, Maybe another try?: "
too_low_text = "Your guess is too low!"
too_high_text = "Your guess is too high!"

player_one_input = int(input("Player one, Please enter your number: "))
print("\n"*100)
player_two_input = int(input("Player two, Please enter your number: "))
while not correct:
    if player_one_input == player_two_input:
        correct = True
        print(correct_text)
        break
    elif player_two_input > player_one_input:
        print(wrong_text.format(too_high_text))
    elif player_two_input < player_one_input:
        print(wrong_text.format(too_low_text))
    player_two_input = int(input())
