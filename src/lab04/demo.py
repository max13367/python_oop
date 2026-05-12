from model import ClientAccount, CreditAccount, SavingsAccount
from typing import List


def sep(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# универсальный вывод через интерфейс
def print_all(items: List):
    print("\n📄 PRINTABLE OUTPUT")
    for i in items:
        print(i.to_string())


# ---------------- SCENARIO 1 ----------------
def scenari_1():
    sep("CREATION")

    a1 = CreditAccount("1111111111", "Ivan", 1000, "USD", 500, 10)
    a2 = SavingsAccount("2222222222", "Maria", 2000, "EUR", 5)

    print(a1)
    print(a2)


# ---------------- SCENARIO 2 ----------------
def scenari_2():
    sep("POLYMORPHISM (PROCESS)")

    accounts = [
        CreditAccount("3333333333", "Alex", -100, "USD", 500, 10),
        SavingsAccount("4444444444", "Bob", 1000, "EUR", 5)
    ]

    for acc in accounts:
        acc.process()


# ---------------- SCENARIO 3 ----------------
def scenari_3():
    sep("INTERFACES (PRINTABLE)")

    accounts = [
        CreditAccount("5555555555", "Chris", 100, "USD", 500, 10),
        SavingsAccount("6666666666", "Dan", 200, "EUR", 5)
    ]

    print_all(accounts)


# ---------------- SCENARIO 4 ----------------
def scenari_4():
    sep("COMPARABLE")

    a1 = CreditAccount("7777777777", "Max", 300, "USD", 500, 10)
    a2 = CreditAccount("8888888888", "Egor", 100, "USD", 500, 10)

    print("A1:", a1.to_string())
    print("A2:", a2.to_string())

    result = a1.compare_to(a2)

    print("\nRESULT:")
    if result == 1:
        print("A1 > A2 (A1 имеет больше баланс)")
    elif result == -1:
        print("A1 < A2 (A2 имеет больше баланс)")
    else:
        print("A1 == A2 (A1 и A2 имеют одинаковый баланс")


# ---------------- MAIN ----------------
def main():
    scenari_1()
    scenari_2()
    scenari_3()
    scenari_4()


if __name__ == "__main__":
    main()