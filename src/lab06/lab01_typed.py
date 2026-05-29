"""
Классы из ЛР-1 с добавленными аннотациями типов
и методами display() / score() для протоколов ЛР-6.
"""

from src.lab01.validate import (
    check_name,
    check_id,
    check_money,
    check_currency,
)


class ClientAccount:
    bank_title: str = "MaxBank"

    def __init__(
        self,
        acc_id: str,
        holder: str,
        balance: float,
        currency: str,
        credit_limit: float = 0.0,
    ) -> None:
        check_id(acc_id)
        check_name(holder)
        check_currency(currency)
        check_money(credit_limit, "Кредитный лимит")

        if balance < -credit_limit:
            raise ValueError("Начальный баланс выходит за пределы кредитного лимита")

        self._id: str = acc_id
        self._holder: str = holder
        self._balance: float = float(balance)
        self._currency: str = currency.upper()
        self._credit_limit: float = float(credit_limit)
        self._active: bool = True

    # properties

    @property
    def holder(self) -> str:
        return self._holder

    @holder.setter
    def holder(self, value: str) -> None:
        check_name(value)
        self._holder = value

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def is_active(self) -> bool:
        return self._active

    # бизнес-методы

    def add_funds(self, amount: float) -> None:
        self._check_active()
        check_money(amount, "Сумма пополнения")
        self._balance += amount

    def withdraw_funds(self, amount: float) -> None:
        self._check_active()
        check_money(amount, "Сумма снятия")
        if self._balance - amount < -self._credit_limit:
            raise ValueError("Недостаточно средств с учётом кредитного лимита")
        self._balance -= amount

    def apply_interest(self, percent: float) -> None:
        self._check_active()
        if self._balance > 0:
            self._balance += self._balance * percent / 100

    def block_account(self) -> None:
        self._active = False

    # методы для протоколов ЛР-6

    def display(self) -> str:
        """Реализует протокол Displayable."""
        return str(self)

    def score(self) -> float:
        """Реализует протокол Scorable — возвращает баланс."""
        return self._balance

    # служебные

    def _check_active(self) -> None:
        if not self._active:
            raise RuntimeError("Счёт заблокирован")

    def __str__(self) -> str:
        status = "ACTIVE" if self._active else "BLOCKED"
        return (
            f"{self.bank_title} | "
            f"{self._holder} | "
            f"{self._balance:.2f} {self._currency} | "
            f"{status}"
        )

    def __repr__(self) -> str:
        return (
            f"ClientAccount('{self._id}', '{self._holder}', "
            f"{self._balance}, '{self._currency}', {self._credit_limit})"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ClientAccount) and self._id == other._id