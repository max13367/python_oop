from typing import List, Callable
from lab01.model import ClientAccount
from lab03.model import CreditAccount, SavingsAccount
from lab07.exceptions import AccountNotFoundError, DuplicateAccountError
import lab07.storage as storage

DATA_FILE = "lab07/accounts.json"


class BankApp:
    """Основной класс приложения. Хранит коллекцию и реализует все операции."""

    def __init__(self) -> None:
        """Инициализация: автоматически загружает данные из файла."""
        self._accounts: List[ClientAccount] = []
        self.load()

    # загрузка / сохранение

    def load(self) -> int:
        """Загрузить данные из файла.

        Returns:
            Количество загруженных счётов.
        """
        self._accounts = storage.load(DATA_FILE)
        return len(self._accounts)

    def save(self) -> None:
        """Сохранить текущую коллекцию в файл."""
        storage.save(self._accounts, DATA_FILE)

    # CRUD

    def add_account(self, account: ClientAccount) -> None:
        """Добавить счёт в коллекцию.

        Raises:
            DuplicateAccountError: счёт с таким ID уже есть.
        """
        if any(a.account_id == account.account_id for a in self._accounts):
            raise DuplicateAccountError(
                f"Счёт с ID '{account.account_id}' уже существует"
            )
        self._accounts.append(account)

    def remove_account(self, acc_id: str) -> ClientAccount:
        """Удалить счёт по ID. Возвращает удалённый объект.

        Raises:
            AccountNotFoundError: счёт не найден.
        """
        acc = self._find_or_raise(acc_id)
        self._accounts.remove(acc)
        return acc

    def get_all(self) -> List[ClientAccount]:
        """Вернуть список всех счётов."""
        return list(self._accounts)

    def find_by_id(self, acc_id: str) -> ClientAccount:
        """Найти счёт по ID.

        Raises:
            AccountNotFoundError: счёт не найден.
        """
        return self._find_or_raise(acc_id)

    # поиск и фильтрация

    def find_by_holder(self, name: str) -> List[ClientAccount]:
        """Найти счета по имени владельца (регистронезависимо)."""
        query = name.lower()
        return [a for a in self._accounts if query in a.holder.lower()]

    def filter_by_currency(self, currency: str) -> List[ClientAccount]:
        """Фильтрация по валюте."""
        return [a for a in self._accounts if a.currency == currency.upper()]

    def filter_by_balance_range(
        self, min_bal: float, max_bal: float
    ) -> List[ClientAccount]:
        """Фильтрация по диапазону баланса."""
        return [a for a in self._accounts if min_bal <= a.balance <= max_bal]

    def filter_active(self, active: bool = True) -> List[ClientAccount]:
        """Фильтрация по статусу счёта."""
        return [a for a in self._accounts if a.is_active == active]

    def filter_by_type(self, acc_type: str) -> List[ClientAccount]:
        """Фильтрация по типу: standard / savings / credit."""
        return [a for a in self._accounts if a.account_type == acc_type]

    # сортировка

    def get_sorted(
        self, key: str = "holder", reverse: bool = False
    ) -> List[ClientAccount]:
        """Вернуть отсортированный список счётов.

        Args:
            key: поле сортировки — holder / balance / acc_id / type.
            reverse: True для сортировки по убыванию.
        """
        key_funcs: dict[str, Callable[[ClientAccount], object]] = {
            "holder":  lambda a: a.holder.lower(),
            "balance": lambda a: a.balance,
            "acc_id":  lambda a: a.account_id,
            "type":    lambda a: a.account_type,
        }
        func = key_funcs.get(key, key_funcs["holder"])
        return sorted(self._accounts, key=func, reverse=reverse)

    # операции со счётом

    def deposit(self, acc_id: str, amount: float) -> None:
        """Пополнить счёт.

        Raises:
            AccountNotFoundError: счёт не найден.
        """
        acc = self._find_or_raise(acc_id)
        acc.add_funds(amount)

    def withdraw(self, acc_id: str, amount: float) -> None:
        """Снять средства со счёта.

        Raises:
            AccountNotFoundError: счёт не найден.
        """
        acc = self._find_or_raise(acc_id)
        acc.withdraw_funds(amount)

    def block(self, acc_id: str) -> None:
        """Заблокировать счёт.

        Raises:
            AccountNotFoundError: счёт не найден.
        """
        acc = self._find_or_raise(acc_id)
        acc.block_account()

    # вспомогательные

    def count(self) -> int:
        """Количество счётов в коллекции."""
        return len(self._accounts)

    def _find_or_raise(self, acc_id: str) -> ClientAccount:
        """Найти счёт или выбросить AccountNotFoundError."""
        for acc in self._accounts:
            if acc.account_id == acc_id:
                return acc
        raise AccountNotFoundError(f"Счёт с ID '{acc_id}' не найден")