from typing import Optional, List
from lab01.model import ClientAccount
from lab03.model import CreditAccount, SavingsAccount
from lab07.app import BankApp
from lab07.exceptions import (
    AccountNotFoundError,
    DuplicateAccountError,
    AccountBlockedError,
    InsufficientFundsError
)


def print_menu() -> None:
    """Вывести главное меню."""
    print("\n" + "=" * 50)
    print("        БАНКОВСКАЯ СИСТЕМА")
    print("=" * 50)
    print("1.  Показать все счета")
    print("2.  Добавить счёт")
    print("3.  Найти счёт по ID")
    print("4.  Найти по владельцу")
    print("5.  Удалить счёт")
    print("6.  Пополнить счёт")
    print("7.  Снять средства")
    print("8.  Заблокировать счёт")
    print("9.  Фильтровать по валюте")
    print("10. Фильтровать по балансу")
    print("11. Фильтровать по типу")
    print("12. Сортировать счета")
    print("0.  Выход")
    print("=" * 50)


def print_account(acc: ClientAccount) -> None:
    """Вывести информацию об одном счёте."""
    status = "✓ Активен" if acc.is_active else "✗ Заблокирован"
    print(f"\nID: {acc.account_id}")
    print(f"Владелец: {acc.holder}")
    print(f"Тип: {acc.account_type}")
    print(f"Баланс: {acc.balance:.2f} {acc.currency}")
    print(f"Статус: {status}")

    if isinstance(acc, CreditAccount):
        print(f"Кредитный лимит: {acc.credit_limit:.2f}")
        print(f"Процентная ставка: {acc.interest_rate}%")
    elif isinstance(acc, SavingsAccount):
        print(f"Процентная ставка: {acc.interest_rate}%")
    print("-" * 50)


def print_accounts(accounts: List[ClientAccount]) -> None:
    """Вывести список счётов."""
    if not accounts:
        print("\n⚠ Счета не найдены.")
        return

    print(f"\n📋 Найдено счетов: {len(accounts)}")
    for acc in accounts:
        print_account(acc)


def input_float(prompt: str) -> float:
    """Ввести число с плавающей точкой с обработкой ошибок."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Ошибка: введите число!")


def input_int(prompt: str) -> int:
    """Ввести целое число с обработкой ошибок."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Ошибка: введите целое число!")


def confirm(prompt: str) -> bool:
    """Запросить подтверждение у пользователя."""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ('y', 'yes', 'д', 'да'):
            return True
        elif answer in ('n', 'no', 'н', 'нет'):
            return False
        else:
            print("Введите y или n")


def add_account_dialog(app: BankApp) -> None:
    """Диалог добавления нового счёта."""
    print("\n--- Добавление счёта ---")
    print("Выберите тип счёта:")
    print("1. Стандартный")
    print("2. Сберегательный")
    print("3. Кредитный")

    acc_type = input_int("Тип счёта: ")

    acc_id = input("ID счёта: ").strip()
    holder = input("Владелец: ").strip()
    balance = input_float("Начальный баланс: ")
    currency = input("Валюта (по умолчанию RUB): ").strip().upper() or "RUB"

    try:
        if acc_type == 1:
            account = ClientAccount(acc_id, holder, balance, currency)
        elif acc_type == 2:
            rate = input_float("Процентная ставка: ")
            account = SavingsAccount(acc_id, holder, balance, currency, interest_rate=rate)
        elif acc_type == 3:
            limit = input_float("Кредитный лимит: ")
            rate = input_float("Процентная ставка: ")
            account = CreditAccount(acc_id, holder, balance, currency, limit, rate)
        else:
            print("❌ Неверный тип счёта!")
            return

        app.add_account(account)
        print(f"✅ Счёт {acc_id} успешно добавлен!")
    except DuplicateAccountError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def run() -> None:
    """Главный цикл приложения."""
    app = BankApp()
    loaded = app.count()
    print(f"\n✅ Загружено счетов: {loaded}")

    while True:
        print_menu()

        try:
            choice = input_int("Выберите пункт: ")
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break

        try:
            if choice == 0:
                if confirm("Сохранить данные перед выходом?"):
                    app.save()
                    print("💾 Данные сохранены.")
                print("👋 До свидания!")
                break

            elif choice == 1:  # Показать все
                print_accounts(app.get_all())

            elif choice == 2:  # Добавить
                add_account_dialog(app)

            elif choice == 3:  # Найти по ID
                acc_id = input("ID счёта: ").strip()
                acc = app.find_by_id(acc_id)
                print_account(acc)

            elif choice == 4:  # Найти по владельцу
                name = input("Имя владельца: ").strip()
                accounts = app.find_by_holder(name)
                print_accounts(accounts)

            elif choice == 5:  # Удалить
                acc_id = input("ID счёта для удаления: ").strip()
                if confirm(f"Удалить счёт {acc_id}?"):
                    acc = app.remove_account(acc_id)
                    print(f"✅ Счёт {acc.account_id} удалён.")

            elif choice == 6:  # Пополнить
                acc_id = input("ID счёта: ").strip()
                amount = input_float("Сумма пополнения: ")
                app.deposit(acc_id, amount)
                print(f"✅ Счёт пополнен на {amount}")

            elif choice == 7:  # Снять
                acc_id = input("ID счёта: ").strip()
                amount = input_float("Сумма снятия: ")
                app.withdraw(acc_id, amount)
                print(f"✅ Снято {amount}")

            elif choice == 8:  # Заблокировать
                acc_id = input("ID счёта: ").strip()
                if confirm(f"Заблокировать счёт {acc_id}?"):
                    app.block(acc_id)
                    print(f"✅ Счёт {acc_id} заблокирован.")

            elif choice == 9:  # Фильтр по валюте
                currency = input("Валюта: ").strip().upper()
                accounts = app.filter_by_currency(currency)
                print_accounts(accounts)

            elif choice == 10:  # Фильтр по балансу
                min_bal = input_float("Минимальный баланс: ")
                max_bal = input_float("Максимальный баланс: ")
                accounts = app.filter_by_balance_range(min_bal, max_bal)
                print_accounts(accounts)

            elif choice == 11:  # Фильтр по типу
                print("Типы: standard / savings / credit")
                acc_type = input("Тип счёта: ").strip()
                accounts = app.filter_by_type(acc_type)
                print_accounts(accounts)

            elif choice == 12:  # Сортировка
                print("Сортировать по:")
                print("1. Владельцу")
                print("2. Балансу")
                print("3. ID")
                print("4. Типу")
                sort_choice = input_int("Выбор: ")

                keys = {1: "holder", 2: "balance", 3: "acc_id", 4: "type"}
                key = keys.get(sort_choice, "holder")

                reverse = confirm("По убыванию?")
                accounts = app.get_sorted(key, reverse)
                print_accounts(accounts)

            else:
                print("❌ Неверный пункт меню!")

        except AccountNotFoundError as e:
            print(f"❌ {e}")
        except (AccountBlockedError, InsufficientFundsError) as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}")