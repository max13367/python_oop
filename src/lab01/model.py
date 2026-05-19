from src.lab01.validate import (
    check_name,
    check_id,
    check_money,
    check_currency
)


class ClientAccount:
    bank_title = "MaxBank"

    def __init__(self, acc_id, holder, balance, currency, credit_limit=0):
        check_id(acc_id)
        check_name(holder)
        check_currency(currency)
        check_money(credit_limit, "Кредитный лимит")

        if balance < -credit_limit:
            raise ValueError("Начальный баланс выходит за пределы кредитного лимита")

        self._id = acc_id
        self._holder = holder
        self._balance = float(balance)
        self._currency = currency.upper()
        self._credit_limit = float(credit_limit)
        self._active = True

    # properties
    @property
    def holder(self):
        return self._holder

    @holder.setter
    def holder(self, value):
        check_name(value)
        self._holder = value

    @property
    def balance(self):
        return self._balance

    @property
    def is_active(self):
        return self._active

    # бизнес-методы
    def add_funds(self, amount):
        self._check_active()
        check_money(amount, "Сумма пополнения")
        self._balance += amount

    def withdraw_funds(self, amount):
        self._check_active()
        check_money(amount, "Сумма снятия")

        if self._balance - amount < -self._credit_limit:
            raise ValueError("Недостаточно средств с учетом кредитного лимита")

        self._balance -= amount

    def apply_interest(self, percent):
        self._check_active()

        if self._balance > 0:
            self._balance += self._balance * percent / 100

    def block_account(self):
        self._active = False

    # служебные
    def _check_active(self):
        if not self._active:
            raise RuntimeError("Счет заблокирован")

    # магические
    def __str__(self):
        status = "ACTIVE" if self._active else "BLOCKED"
        return (
            f"{self.bank_title} | "
            f"{self._holder} | "
            f"{self._balance:.2f} {self._currency} | "
            f"{status}"
        )

    def __repr__(self):
        return (
            f"ClientAccount('{self._id}', '{self._holder}', "
            f"{self._balance}, '{self._currency}', {self._credit_limit})"
        )

    def __eq__(self, other):
        return isinstance(other, ClientAccount) and self._id == other._id