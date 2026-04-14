from model import Account


class AccountStorage:
    def __init__(self):
        self._data = []

    # добавление
    def append(self, account: Account):
        if not isinstance(account, Account):
            raise TypeError("Допускаются только объекты Account")

        # проверка уникальности по номеру
        for item in self._data:
            if item.account_number == account.account_number:
                raise ValueError("Такой счет уже есть")

        self._data.append(account)

    # удаление
    def delete(self, account: Account):
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
    def get_by_number(self, number: str):
        return next((acc for acc in self._data if acc.account_number == number), None)

    def get_by_owner(self, name: str):
        result = []
        for acc in self._data:
            if acc.owner == name:
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

    def order_by_owner(self):
        self._data.sort(key=lambda x: x.owner.lower())

    # фильтрация
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

    def with_min_balance(self, amount: float):
        new_storage = AccountStorage()
        for acc in self._data:
            if acc.balance >= amount:
                new_storage.append(acc)
        return new_storage