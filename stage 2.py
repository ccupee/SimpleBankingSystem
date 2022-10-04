from random import randint


database = []


#According to Luhn Algorithm
def luhn_alg(num):
    number = [elem for elem in num]
    for i in range(0, len(number), 2):
        number[i] = str(int(number[i]) * 2)
    for i in range(len(number)):
        if int(number[i]) > 9:
            number[i] = str(int(number[i]) - 9)
    return sum([int(x) for x in number])


def generating_number():
    iin = '400000'  #Issuer Identification Number
    cu_ac_num = ''.join(str(randint(0, 9)) for _ in range(9))  #Customer Account Number
    i = 0  #Checksum
    while True:
        first_sum = luhn_alg(iin + cu_ac_num + str(i))
        if first_sum % 10 == 0:
            break
        else:
            i += 1
            continue
    return iin + cu_ac_num + str(i)


def check_luhn_alg(number):
    return luhn_alg(number) % 10 == 0


def start_menu(cards):
    while True:
        choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
        if choice == 1:
            card_number = generating_number()
            pin = ''.join(str(randint(0, 9)) for _ in range(4))
            cards.append({"number": card_number, "pin": pin, "balance": 0})
            print(f'''Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}''')
            continue
        elif choice == 2:
            number, pin = input("Enter your card number:\n"), input("Enter your PIN:\n")
            if not check_luhn_alg(number):
                print("\nWrong card number or PIN!")
                continue
            if number not in [elem["number"] for elem in cards] or pin not in [elem["pin"] for elem in cards]:
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


def main():
    start_menu(database)


if __name__ == '__main__':
    main()
    