from random import randint
import sqlite3


database = []
db_creation = '''CREATE TABLE IF NOT EXISTS card
    (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );'''


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


def new_card(cards, cur, conn):
    card_number = generating_number()
    pin = ''.join(str(randint(0, 9)) for _ in range(4))
    cards.append({"number": card_number, "pin": pin, "balance": 0})
    user_id = randint(0, 1000000)
    cur.execute(f'INSERT INTO card VALUES ({user_id}, {card_number}, {pin}, 0);')
    print(f'''Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}''')
    conn.commit()


def income(cards, number, cur, conn):
    incoming = int(input("Enter income:\n"))
    cur.execute(f'UPDATE card SET balance = balance + {incoming} WHERE number = {number};')
    conn.commit()
    for elem in cards:
        if elem["number"] == number:
            elem["balance"] += incoming
    print("Income was added!\n")


def transfer(cards, number, cur, conn):
    new_number = input("Transfer\nEnter card number:\n")
    if new_number == number:
        print("You can't transfer money to the same account!\n")
        return False
    elif not check_luhn_alg(new_number):
        print("Probably you made a mistake in the card number. Please try again!\n")
        return False
    elif new_number not in [elem["number"] for elem in cards]:
        print("Such a card does not exist.\n")
        return False
    else:
        money = int(input("Enter how much money you want to transfer:\n"))
        amount = [elem["balance"] for elem in cards if elem["number"] == number][0]
        if amount < money:
            print("Not enough money!\n")
            return False
        cur.execute(f'UPDATE card SET balance = balance + {money} WHERE number = {new_number};')
        cur.execute(f'UPDATE card SET balance = balance - {money} WHERE number = {number}')
        conn.commit()
        for elem in cards:
            if elem["number"] == new_number:
                elem["balance"] += money
            if elem["number"] == number:
                elem["balance"] -= money
        print("Success!\n")


def deleting_account(cards, number, cur, conn):
    cur.execute(f'DELETE FROM card WHERE number = {number};')
    conn.commit()
    for elem in cards:
        if elem["number"] == number:
            cards.remove(elem)
    print("The account has been closed!\n")


def menu(cards, cur, conn):
    while True:
        choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
        if choice == 1:
            new_card(cards, cur, conn)
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
                if second_menu(cards, cur, conn, number) == -1:
                    break
        else:
            print("\nBye!")
            break


def second_menu(cards, cur, conn, number):
    while True:
        choice = int(input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"))
        if choice == 1:
            print("Balance:", [elem["balance"] for elem in cards], end='\n')
            continue
        elif choice == 2:
            income(cards, number, cur, conn)
            continue
        elif choice == 3:
            if not transfer(cards, number, cur, conn):
                continue
        elif choice == 4:
            deleting_account(cards, number, cur, conn)
            break
        elif choice == 5:
            print("\nYou have successfully logged out!")
            break
        else:
            print("\nBye!")
            return -1


def main():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute(db_creation)
    menu(database, cur, conn)
    conn.close()


if __name__ == '__main__':
    main()
    