from lab01.model import ClientAccount


class CreditAccount(ClientAccount):
    def __init__(self, acc_id: str, holder: str, balance: float,
                 currency: str, credit_limit: float,
                 interest_rate: float) -> None:
        super().__init__(acc_id, holder, balance, currency, credit_limit)
        self._interest_rate: float = interest_rate
        self._fee: float = 0.1

    @property
    def account_type(self) -> str:
        return "credit"

    @property
    def interest_rate(self) -> float:
        return self._interest_rate

    @property
    def credit_limit(self) -> float:
        return self._credit_limit

    def process(self) -> None:
        self.apply_interest()

    def apply_interest(self, percent: float = 0) -> None:
        self._check_active()
        if self._balance < 0:
            interest = abs(self._balance) * self._interest_rate / 100
            self._balance -= interest

    def withdraw_funds(self, amount: float) -> None:
        self._check_active()
        fee = amount * self._fee
        if self._balance - amount - fee < -self._credit_limit:
            raise ValueError("Превышен лимит")
        self._balance -= (amount + fee)

    # ── сериализация ─────────────────────────────────────────

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["interest_rate"] = self._interest_rate
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "CreditAccount":
        obj = cls(
            data["acc_id"],
            data["holder"],
            data["balance"],
            data["currency"],
            data.get("credit_limit", 0),
            data["interest_rate"],
        )
        if not data.get("is_active", True):
            obj._active = False
        return obj

    def __str__(self) -> str:
        return super().__str__() + f" | Credit ({self._interest_rate}%)"


class SavingsAccount(ClientAccount):
    def __init__(self, acc_id: str, holder: str, balance: float,
                 currency: str, interest_rate: float) -> None:
        super().__init__(acc_id, holder, balance, currency)
        self._interest_rate: float = interest_rate
        self._bonus: float = 0.02

    @property
    def account_type(self) -> str:
        return "savings"

    @property
    def interest_rate(self) -> float:
        return self._interest_rate

    def process(self) -> None:
        self.apply_interest()

    def apply_interest(self, percent: float = 0) -> None:
        self._check_active()
        if self._balance > 0:
            self._balance += self._balance * self._interest_rate / 100

    def add_funds(self, amount: float) -> None:
        self._check_active()
        bonus = amount * self._bonus
        self._balance += amount + bonus

    # ── сериализация ─────────────────────────────────────────

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["interest_rate"] = self._interest_rate
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "SavingsAccount":
        obj = cls(
            data["acc_id"],
            data["holder"],
            data["balance"],
            data["currency"],
            data["interest_rate"],
        )
        if not data.get("is_active", True):
            obj._active = False
        return obj

    def __str__(self) -> str:
        return super().__str__() + f" | Savings ({self._interest_rate}%)"