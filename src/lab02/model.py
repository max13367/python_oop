from validate import (
    validate_account_id,
    validate_owner_name,
    validate_money,
    ensure_currency,
)


class Account:
    BANK_NAME = "MaxBank"

    def __init__(self, acc_id, owner, amount, currency, credit_limit=0):
        validate_account_id(acc_id)
        validate_owner_name(owner)
        ensure_currency(currency)
        validate_money(credit_limit, "Кредитный лимит")

        if amount < -credit_limit:
            raise ValueError("Начальный баланс выходит за допустимый предел")

        self._id = acc_id
        self._owner = owner
        self._amount = float(amount)
        self._currency = currency.upper()
        self._limit = float(credit_limit)
        self._active = True

    # --- свойства ---
    @property
    def account_number(self):
        return self._id

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_value):
        validate_owner_name(new_value)
        self._owner = new_value

    @property
    def balance(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    @property
    def is_active(self):
        return self._active

    # --- методы ---
    def deposit(self, value):
        self._check_state()
        validate_money(value, "Пополнение")
        self._amount += value

    def withdraw(self, value):
        self._check_state()
        validate_money(value, "Снятие")

        if self._amount - value < -self._limit:
            raise ValueError("Недостаточно средств")

        self._amount -= value

    def close(self):
        self._active = False

    # --- внутреннее ---
    def _check_state(self):
        if not self._active:
            raise RuntimeError("Счет не активен")

    # --- магические ---
    def __str__(self):
        state = "OPEN" if self._active else "CLOSED"
        return (
            f"{self.BANK_NAME} | "
            f"{self._owner} | "
            f"{self._amount:.2f} {self._currency} | "
            f"{state}"
        )

    def __repr__(self):
        return (
            f"Account('{self._id}', '{self._owner}', "
            f"{self._amount}, '{self._currency}', {self._limit})"
        )

    def __eq__(self, other):
        return isinstance(other, Account) and self._id == other._id