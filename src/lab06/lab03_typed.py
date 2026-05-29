from lab06.lab01_typed import ClientAccount


class CreditAccount(ClientAccount):
    def __init__(
        self,
        acc_id: str,
        holder: str,
        balance: float,
        currency: str,
        credit_limit: float,
        interest_rate: float,
    ) -> None:
        super().__init__(acc_id, holder, balance, currency, credit_limit)
        self._interest_rate: float = interest_rate
        self._fee: float = 0.1

    def process(self) -> None:
        self.apply_interest()

    def apply_interest(self, percent: float = 0.0) -> None:  # type: ignore[override]
        self._check_active()
        if self._balance < 0:
            interest: float = abs(self._balance) * self._interest_rate / 100
            self._balance -= interest

    def withdraw_funds(self, amount: float) -> None:
        self._check_active()
        fee: float = amount * self._fee
        if self._balance - amount - fee < -self._credit_limit:
            raise ValueError("Превышен лимит")
        self._balance -= amount + fee

    def score(self) -> float:
        """Для кредитного счёта скоринг — это кредитный лимит."""
        return self._credit_limit

    def __str__(self) -> str:
        return super().__str__() + f" | Credit ({self._interest_rate}%)"


class SavingsAccount(ClientAccount):
    def __init__(
        self,
        acc_id: str,
        holder: str,
        balance: float,
        currency: str,
        interest_rate: float,
    ) -> None:
        super().__init__(acc_id, holder, balance, currency)
        self._interest_rate: float = interest_rate
        self._bonus: float = 0.02

    def process(self) -> None:
        self.apply_interest()

    def apply_interest(self, percent: float = 0.0) -> None:  # type: ignore[override]
        self._check_active()
        if self._balance > 0:
            self._balance += self._balance * self._interest_rate / 100

    def add_funds(self, amount: float) -> None:
        self._check_active()
        bonus: float = amount * self._bonus
        self._balance += amount + bonus

    def score(self) -> float:
        """Для накопительного счёта скоринг учитывает потенциальный доход."""
        return self._balance + self._balance * self._interest_rate / 100

    def __str__(self) -> str:
        return super().__str__() + f" | Savings ({self._interest_rate}%)"