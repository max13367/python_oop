from validate import check_name, check_id, check_money, check_currency
from interfaces import Printable, Withdrawable, Comparable, Processable


class ClientAccount(Printable, Withdrawable, Comparable):
    bank_title = "MaxBank"

    def __init__(self, acc_id, holder, balance, currency, credit_limit=0):
        check_id(acc_id)
        check_name(holder)
        check_currency(currency)
        check_money(credit_limit, "credit_limit")

        if balance < -credit_limit:
            raise ValueError("Balance exceeds credit limit")

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

    @property
    def balance(self):
        return self._balance

    @property
    def is_active(self):
        return self._active

    # интерфейс Printable
    def to_string(self) -> str:
        status = "ACTIVE" if self._active else "BLOCKED"
        return f"{self._holder} | {self._balance:.2f} {self._currency} | {status}"

    # интерфейс Comparable
    def compare_to(self, other):
        if not isinstance(other, ClientAccount):
            raise TypeError("Можно сравнивать только аккаунты")

        if self._balance < other._balance:
            return -1
        elif self._balance > other._balance:
            return 1
        return 0

    # интерфейс Withdrawable
    def withdraw_funds(self, amount):
        self._check_active()
        check_money(amount, "withdraw")

        if self._balance - amount < -self._credit_limit:
            raise ValueError("Недостаточно денег")

        self._balance -= amount

    def _check_active(self):
        if not self._active:
            raise RuntimeError("Аккаунт заблокирован")

    def __str__(self):
        return self.to_string()


# ---------------- CREDIT ----------------

class CreditAccount(ClientAccount, Processable):
    def __init__(self, acc_id, holder, balance, currency, credit_limit, interest_rate):
        super().__init__(acc_id, holder, balance, currency, credit_limit)
        self._interest_rate = interest_rate
        self._fee = 0.1

    def process(self):
        print(f"[Credit BEFORE] {self._holder}: {self._balance:.2f}")
        self.apply_interest()
        print(f"[Credit AFTER]  {self._holder}: {self._balance:.2f}")

    def apply_interest(self):
        self._check_active()
        if self._balance < 0:
            interest = abs(self._balance) * self._interest_rate / 100
            self._balance -= interest

    def withdraw_funds(self, amount):
        self._check_active()
        fee = amount * self._fee

        if self._balance - amount - fee < -self._credit_limit:
            raise ValueError("Лимит превышен")

        self._balance -= (amount + fee)

    def __str__(self):
        return super().__str__() + f" | CREDIT {self._interest_rate}%"


# ---------------- SAVINGS ----------------

class SavingsAccount(ClientAccount, Processable):
    def __init__(self, acc_id, holder, balance, currency, interest_rate):
        super().__init__(acc_id, holder, balance, currency)
        self._interest_rate = interest_rate
        self._bonus = 0.02

    def process(self):
        print(f"[Savings BEFORE] {self._holder}: {self._balance:.2f}")
        self.apply_interest()
        print(f"[Savings AFTER]  {self._holder}: {self._balance:.2f}")

    def apply_interest(self):
        self._check_active()
        if self._balance > 0:
            self._balance += self._balance * self._interest_rate / 100

    def add_funds(self, amount):
        self._check_active()
        self._balance += amount + amount * self._bonus

    def __str__(self):
        return super().__str__() + f" | SAVINGS {self._interest_rate}%"