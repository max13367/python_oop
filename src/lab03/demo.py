from model import CreditAccount, SavingsAccount
from collection import AccountStorage


def main():
    storage = AccountStorage()

    acc1 = CreditAccount("1234567890", "Max", -200, "USD", 1000, 10)
    acc2 = SavingsAccount("0987654321", "Anna", 500, "EUR", 5)
    acc3 = CreditAccount("1111111111", "John", 0, "USD", 500, 15)

    storage.append(acc1)
    storage.append(acc2)
    storage.append(acc3)

    print("=== Все счета ===")
    for acc in storage:
        print(acc)

    print("\n=== Полиморфизм (process) ===")
    for acc in storage:
        acc.process()

    for acc in storage:
        print(acc)

    print("\n=== Фильтрация ===")
    credit_accounts = storage.only_credit()
    savings_accounts = storage.only_savings()

    print("Кредитные:")
    for acc in credit_accounts:
        print(acc)

    print("Накопительные:")
    for acc in savings_accounts:
        print(acc)

    print("\n=== Работа методов ===")
    acc1.withdraw_funds(100)
    acc2.add_funds(200)

    for acc in storage:
        print(acc)

    print("\n=== Проверка типов ===")
    for acc in storage:
        if isinstance(acc, CreditAccount):
            print(f"{acc.holder} -> Credit")
        elif isinstance(acc, SavingsAccount):
            print(f"{acc.holder} -> Savings")


if __name__ == "__main__":
    main()