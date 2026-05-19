from src.lab01.model import ClientAccount
from src.lab03.model import CreditAccount, SavingsAccount
from src.lab05.collection import AccountStorage
import src.lab05.strategies as st

def header(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)


def create_data():
    storage = AccountStorage()

    a1 = ClientAccount("ACC0000001", "Иванов", 50000, "rub")
    a2 = SavingsAccount("ACC0000002", "Петрова", 120000, "rub", 5)
    a3 = CreditAccount("ACC0000003", "Сидоров", -20000, "rub", 100000, 10)
    a4 = ClientAccount("ACC0000004", "Кузнецова", 250000, "rub")
    a5 = ClientAccount("ACC0000005", "Смирнов", 8000, "rub")

    a5.block_account()

    for acc in [a1, a2, a3, a4, a5]:
        storage.append(acc)

    return storage


# -------- СЦЕНАРИЙ 1 --------

def scenario_sort(storage):
    header("СОРТИРОВКА")

    print("По балансу:")
    data = storage.all()
    data.sort(key=st.sort_by_balance)
    for acc in data:
        print(acc)

    print("\nПо имени (lambda):")
    data = sorted(storage.all(), key=lambda x: x.holder)
    for acc in data:
        print(acc)

    print("\nПо статусу + балансу:")
    data = sorted(storage.all(), key=st.sort_by_state_and_balance)
    for acc in data:
        print(acc)


# -------- СЦЕНАРИЙ 2 --------

def scenario_filter(storage):
    header("ФИЛЬТРАЦИЯ")

    active = list(filter(st.account_active, storage.all()))
    print("Активные:")
    for a in active:
        print(a)

    print("\nС балансом > 10000:")
    filt = st.build_balance_filter(10000)
    result = list(filter(filt, storage.all()))
    for a in result:
        print(a)


# -------- СЦЕНАРИЙ 3 --------

def scenario_map(storage):
    header("MAP")

    print("Короткий вывод:")
    res = list(map(st.to_short, storage.all()))
    for r in res:
        print(r)

    print("\nИмена:")
    names = list(map(lambda x: x.holder, storage.all()))
    print(names)


# -------- СЦЕНАРИЙ 4 --------

def scenario_chain(storage):
    header("ЦЕПОЧКА")

    result = (
        storage
        .filter_by(st.account_active)
        .sort_by(st.sort_by_balance_desc)
        .apply(st.to_short)
    )

    for r in result:
        print(r)


# -------- СЦЕНАРИЙ 5 --------

def scenario_strategy(storage):
    header("СТРАТЕГИИ")

    basic = st.BasicInterest()
    bonus = st.BonusInterest()

    for acc in storage.all():
        print(acc.holder)
        print("  basic:", basic(acc))
        print("  bonus:", bonus(acc))


def main():
    storage = create_data()

    scenario_sort(storage)
    scenario_filter(storage)
    scenario_map(storage)
    scenario_chain(storage)
    scenario_strategy(storage)


if __name__ == "__main__":
    main()