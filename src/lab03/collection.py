from base import ClientAccount
from model import CreditAccount, SavingsAccount


class AccountStorage:
    def __init__(self):
        self._data = []

    # добавление
    def append(self, account: ClientAccount):
        if not isinstance(account, ClientAccount):
            raise TypeError("Допускаются только объекты ClientAccount")

        # уникальность по id
        for item in self._data:
            if item._id == account._id:
                raise ValueError("Такой счет уже существует")

        self._data.append(account)

    # удаление
    def delete(self, account: ClientAccount):
        if account in self._data:
            self._data.remove(account)

    def delete_by_index(self, idx: int):
        if idx < 0 or idx >= len(self._data):
            raise IndexError("Индекс вне диапазона")
        self._data.pop(idx)

    # получение
    def all(self):
        return list(self._data)

    def __getitem__(self, index):
        return self._data[index]

    # поиск
    def get_by_id(self, acc_id: str):
        return next((acc for acc in self._data if acc._id == acc_id), None)

    def get_by_holder(self, name: str):
        result = []
        for acc in self._data:
            if acc.holder == name:
                result.append(acc)
        return result

    # итерация
    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for item in self._data:
            yield item

    # сортировка
    def sort_accounts(self, key_func=None):
        self._data.sort(key=key_func)

    def order_by_balance(self):
        self._data.sort(key=lambda x: x.balance)

    def order_by_holder(self):
        self._data.sort(key=lambda x: x.holder.lower())

    # фильтрация по статусу
    def only_active(self):
        new_storage = AccountStorage()
        for acc in self._data:
            if acc.is_active:
                new_storage.append(acc)
        return new_storage

    def only_blocked(self):
        new_storage = AccountStorage()
        for acc in self._data:
            if not acc.is_active:
                new_storage.append(acc)
        return new_storage

    # фильтрация по типу
    def only_credit(self):
        new_storage = AccountStorage()
        for acc in self._data:
            if isinstance(acc, CreditAccount):
                new_storage.append(acc)
        return new_storage

    def only_savings(self):
        new_storage = AccountStorage()
        for acc in self._data:
            if isinstance(acc, SavingsAccount):
                new_storage.append(acc)
        return new_storage

    # фильтр по балансу
    def with_min_balance(self, amount: float):
        new_storage = AccountStorage()
        for acc in self._data:
            if acc.balance >= amount:
                new_storage.append(acc)
        return new_storage

    # полиморфизм
    def process_all(self):
        for acc in self._data:
            acc.process()  # БЕЗ if — это ключевое требование