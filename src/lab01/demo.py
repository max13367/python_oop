from model import ClientAccount


def main():
    print("=== Создание счета ===")
    acc = ClientAccount("1111111111", "Иван Петров", 1000, "USD", 500)
    print(acc)

    print("\n=== Пополнение ===")
    acc.add_funds(500)
    print(acc)

    print("\n=== Снятие ===")
    acc.withdraw_funds(1200)
    print(acc)

    print("\n=== Начисление процентов ===")
    acc.apply_interest(10)
    print(acc)

    print("\n=== Сравнение счетов ===")
    acc2 = ClientAccount("1111111111", "Другой", 0, "USD")
    print("Равны:", acc == acc2)

    print("\n=== Изменение владельца ===")
    acc.holder = "Алексей Смирнов"
    print(acc)

    print("\n=== Блокировка счета ===")
    acc.block_account()
    print(acc)

    try:
        acc.add_funds(100)
    except RuntimeError as e:
        print("Ошибка:", e)

    print("\n=== Ошибка создания ===")
    try:
        bad = ClientAccount("123", "", -1000, "BTC")
    except Exception as e:
        print("Ошибка:", e)

    print("\n=== Атрибут класса ===")
    print("Через класс:", ClientAccount.bank_title)
    print("Через объект:", acc.bank_title)


if __name__ == "__main__":
    main()