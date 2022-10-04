from random import randint


database = []


def second_menu(cards):
    while True:
        choice = int(input("1. Balance\n2. Log out\n0. Exit\n"))
        if choice == 1:
            print("Balance:", [elem["balance"] for elem in cards])
            continue
        elif choice == 2:
            print("\nYou have successfully logged out!")
            break
        else:
            print("\nBye!")
            return -1


def start_menu(cards):
    while True:
        choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
        if choice == 1:
            card_number = '400000' + ''.join(str(randint(0, 9)) for _ in range(10))
            pin = ''.join(str(randint(0, 9)) for _ in range(4))
            cards.append({"number": card_number, "pin": pin, "balance": 0})
            print(f'''Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}''')
            continue
        elif choice == 2:
            number, pin = input("Enter your card number:\n"), input("Enter your PIN:\n")
            if number not in [elem["number"] for elem in cards] \
                    or pin not in [elem["pin"] for elem in cards]:
                print("\nWrong card number or PIN!")
                continue
            else:
                print("\nYou have successfully logged in!")
                print()
                if second_menu(cards) == -1:
                    break
        else:
            print("\nBye!")
            break


start_menu(database)
