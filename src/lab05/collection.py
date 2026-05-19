from src.lab01.model import ClientAccount


class AccountStorage:
    def __init__(self):
        self._data = []

    # добавление
    def append(self, account: ClientAccount):
        if not isinstance(account, ClientAccount):
            raise TypeError("Можно добавлять только ClientAccount")

        for item in self._data:
            if item._id == account._id:
                raise ValueError("Счет уже существует")

        self._data.append(account)
        return self

    # получение
    def all(self):
        return list(self._data)


    def sort_by(self, key_func, reverse=False):
        self._data.sort(key=key_func, reverse=reverse)
        return self

    def filter_by(self, func):
        new_storage = AccountStorage()
        for acc in self._data:
            if func(acc):
                new_storage.append(acc)
        return new_storage

    def apply(self, func):
        result = []
        for acc in self._data:
            result.append(func(acc))
        return result

    # -------- базовое --------

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for item in self._data:
            yield item

    def __str__(self):
        if not self._data:
            return "Пусто"
        return "\n".join(str(x) for x in self._data)