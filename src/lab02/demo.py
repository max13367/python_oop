from model import Account
from collection import AccountStorage


def show(storage, title):
    print(f"\n>>> {title}")
    for acc in storage:
        print(acc)


def main():
    storage = AccountStorage()

    a1 = Account("1111111111", "Max", 1000, "USD", 500)
    a2 = Account("2222222222", "John", 500, "EUR", 1000)
    a3 = Account("3333333333", "Max", 200, "USD", 300)

    print("\n=== Сценарий 1 ===")
    storage.append(a1)
    storage.append(a2)
    storage.append(a3)

    show(storage, "Все счета")

    print("\n=== Сценарий 2 ===")
    print("Найден:", storage.get_by_number("1111111111"))
    print("Счета Max:", storage.get_by_owner("Max"))
    print("Первый:", storage[0])

    storage.delete_by_index(1)
    show(storage, "После удаления")

    print("\n=== Сценарий 3 ===")
    storage.order_by_balance()
    show(storage, "По балансу")

    storage.order_by_owner()
    show(storage, "По владельцу")

    show(storage.with_min_balance(500), "Баланс >= 500")

    a3.close()
    show(storage.only_active(), "Активные")
    show(storage.only_blocked(), "Закрытые")

    print("\n=== Ошибка ===")
    try:
        storage.append(Account("3333333333", "Max", 999, "USD", 100))
    except ValueError as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()