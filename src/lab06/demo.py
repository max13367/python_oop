from lab06.lab01_typed import ClientAccount
from lab06.lab03_typed import CreditAccount, SavingsAccount
from lab06.container import TypedCollection, Displayable, Scorable


def separator(title: str) -> None:
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")



#  Сценарий 1: базовая типизированная коллекция


def scenario_basic() -> None:
    separator("Сценарий 1 — TypedCollection[ClientAccount]")

    accounts: TypedCollection[ClientAccount] = TypedCollection()

    accounts.append(ClientAccount("1000000001", "Максим Орлов", 15000.0, "RUB"))
    accounts.append(SavingsAccount("1000000002", "Анна Смирнова", 80000.0, "RUB", 7.5))
    accounts.append(CreditAccount("1000000003", "Олег Чернов", -3000.0, "RUB", 50000.0, 20.0))

    print(accounts)

    # демонстрация что в коллекцию нельзя добавить что угодно
    # (статически mypy выдаст ошибку, в рантайме Python duck-typed)
    print(f"\nВсего счетов: {len(accounts)}")
    print(f"Первый элемент: {accounts[0]}")



#  Сценарий 2: функциональные методы + TypeVar R


def scenario_functional() -> None:
    separator("Сценарий 2 — find / filter / map")

    col: TypedCollection[ClientAccount] = TypedCollection()
    col.append(ClientAccount("2000000001", "Максим Орлов", 15000.0, "RUB"))
    col.append(SavingsAccount("2000000002", "Анна Смирнова", 80000.0, "RUB", 7.5))
    col.append(CreditAccount("2000000003", "Олег Чернов", -3000.0, "RUB", 50000.0, 20.0))
    col.append(ClientAccount("2000000004", "Ирина Белова", 500.0, "USD"))

    # find
    print("\n▸ find() — поиск счёта Анны Смирновой:")
    found = col.find(lambda acc: acc.holder == "Анна Смирнова")
    print(f"  Найден:  {found}")

    print("\n▸ find() — поиск несуществующего владельца:")
    not_found = col.find(lambda acc: acc.holder == "Владимир Пустой")
    print(f"  Результат: {not_found}")   # None

    # filter
    print("\n▸ filter() — только счета в RUB:")
    rub_accounts = col.filter(lambda acc: acc.currency == "RUB")
    for acc in rub_accounts:
        print(f"  {acc}")

    print("\n▸ filter() — только счета с положительным балансом:")
    positive = col.filter(lambda acc: acc.balance > 0)
    for acc in positive:
        print(f"  {acc}")

    # map TypeVar R меняет тип результата
    print("\n▸ map() → list[str]  (имена владельцев):")
    names: list[str] = col.map(lambda acc: acc.holder)
    print(f"  {names}")

    print("\n▸ map() → list[float]  (балансы):")
    balances: list[float] = col.map(lambda acc: acc.balance)
    print(f"  {balances}")

    print("\n▸ map() → list[bool]  (активность счёта):")
    active_flags: list[bool] = col.map(lambda acc: acc.is_active)
    print(f"  {active_flags}")

    # итог: одна коллекция, три разных типа результата map()
    print(
        "\n  map() вернул str, float и bool из одной TypedCollection[ClientAccount] —"
        "\n  это наглядно показывает зачем нужен второй TypeVar R."
    )


#  Сценарий 3: Protocol Displayable

def scenario_displayable() -> None:
    separator("Сценарий 3 — Protocol Displayable (TypedCollection[D])")

    print(
        "\n  ClientAccount, SavingsAccount, CreditAccount НЕ наследуются от Displayable."
        "\n  Но у каждого есть метод display() — этого достаточно."
    )

    # TypedCollection[D], где D bound=Displayable
    display_col: TypedCollection[Displayable] = TypedCollection()

    acc1 = ClientAccount("3000000001", "Максим Орлов", 15000.0, "RUB")
    acc2 = SavingsAccount("3000000002", "Анна Смирнова", 80000.0, "RUB", 7.5)
    acc3 = CreditAccount("3000000003", "Олег Чернов", -3000.0, "RUB", 50000.0, 20.0)

    # проверка через isinstance работает благодаря @runtime_checkable
    for obj in (acc1, acc2, acc3):
        print(f"\n  isinstance({obj.__class__.__name__}, Displayable) → "
              f"{isinstance(obj, Displayable)}")

    display_col.append(acc1)
    display_col.append(acc2)
    display_col.append(acc3)

    print("\n▸ Вызов display() для каждого элемента коллекции:")
    for item in display_col:
        print(f"  [{item.__class__.__name__:15}]  {item.display()}")


#  Сценарий 4: Protocol Scorable

def scenario_scorable() -> None:
    separator("Сценарий 4 — Protocol Scorable (TypedCollection[S])")

    print(
        "\n  Тот же класс TypedCollection, другое ограничение TypeVar."
        "\n  score() у каждого типа считается по-своему:"
        "\n    ClientAccount  → баланс"
        "\n    SavingsAccount → баланс + потенциальный доход"
        "\n    CreditAccount  → кредитный лимит"
    )

    score_col: TypedCollection[Scorable] = TypedCollection()

    score_col.append(ClientAccount("4000000001", "Максим Орлов", 15000.0, "RUB"))
    score_col.append(SavingsAccount("4000000002", "Анна Смирнова", 80000.0, "RUB", 7.5))
    score_col.append(CreditAccount("4000000003", "Олег Чернов", -3000.0, "RUB", 50000.0, 20.0))

    print("\n▸ score() для каждого элемента:")
    for item in score_col:
        print(f"  [{item.__class__.__name__:15}]  score = {item.score():.2f}")

    # map() внутри Scorable-коллекции
    scores: list[float] = score_col.map(lambda item: item.score())
    print(f"\n▸ map(score) → list[float]: {scores}")

    best = score_col.find(lambda item: item.score() == max(scores))
    print(f"\n▸ Лучший скоринг: {best.__class__.__name__}  score = {best.score():.2f}")


if __name__ == "__main__":
    scenario_basic()
    scenario_functional()
    scenario_displayable()
    scenario_scorable()