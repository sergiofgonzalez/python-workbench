from random import randint

consecutive_throws_count: int = 0
while True:
    dice_throw: int = randint(1, 6)
    print(f"You obtained {dice_throw}")
    if dice_throw % 2 == 0:
        consecutive_throws_count += 1
    else:
        print(f"You reached {consecutive_throws_count} consecutive throws")
        quit(1)
