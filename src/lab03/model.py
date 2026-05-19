from src.lab01.model import ClientAccount

class CreditAccount(ClientAccount):
    def __init__(self, acc_id, holder, balance, currency, credit_limit, interest_rate):
        super().__init__(acc_id, holder, balance, currency, credit_limit)
        self._interest_rate = interest_rate
        self._fee = 0.1

    def process(self):
        # общий интерфейс
        self.apply_interest()

    def apply_interest(self):
        self._check_active()
        if self._balance < 0:
            interest = abs(self._balance) * self._interest_rate / 100
            self._balance -= interest

    def withdraw_funds(self, amount):
        self._check_active()
        fee = amount * self._fee

        if self._balance - amount - fee < -self._credit_limit:
            raise ValueError("Превышен лимит")

        self._balance -= (amount + fee)

    def __str__(self):
        return super().__str__() + f" | Credit ({self._interest_rate}%)"


class SavingsAccount(ClientAccount):
    def __init__(self, acc_id, holder, balance, currency, interest_rate):
        super().__init__(acc_id, holder, balance, currency)
        self._interest_rate = interest_rate
        self._bonus = 0.02

    def process(self):
        self.apply_interest()

    def apply_interest(self):
        self._check_active()
        if self._balance > 0:
            self._balance += self._balance * self._interest_rate / 100

    def add_funds(self, amount):
        self._check_active()
        bonus = amount * self._bonus
        self._balance += amount + bonus

    def __str__(self):
        return super().__str__() + f" | Savings ({self._interest_rate}%)"