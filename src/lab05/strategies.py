# -------- сортировка --------

def sort_by_balance(acc):
    return acc.balance


def sort_by_holder(acc):
    return acc.holder.lower()


def sort_by_balance_desc(acc):
    return acc.balance * -1


def sort_by_state_and_balance(acc):
    # активные сначала
    priority = 0 if acc.is_active else 1
    return (priority, acc.balance * -1)


# -------- фильтры --------

def account_active(acc):
    return acc.is_active


def account_with_money(acc):
    return acc.balance > 0


# -------- фабрики --------

def build_balance_filter(min_val, max_val=None):
    if max_val is None:
        max_val = float("inf")

    def inner(acc):
        return min_val <= acc.balance <= max_val

    return inner


def build_interest_applier(percent):
    def inner(acc):
        new_balance = acc.balance + acc.balance * percent / 100
        return {
            "owner": acc.holder,
            "before": acc.balance,
            "after": new_balance
        }

    return inner


# -------- map --------

def to_short(acc):
    return f"{acc.holder}: {acc.balance:.2f}"


def to_dict(acc):
    return {
        "id": acc._id,
        "holder": acc.holder,
        "balance": acc.balance,
        "active": acc.is_active
    }


# -------- стратегии (callable) --------

class BasicInterest:
    def __call__(self, acc):
        if not acc.is_active:
            return 0
        return acc.balance * 0.03


class BonusInterest:
    def __init__(self, limit=50000):
        self.limit = limit

    def __call__(self, acc):
        if not acc.is_active:
            return 0

        percent = 0.03
        if acc.balance > self.limit:
            percent += 0.02

        return acc.balance * percent


class NoInterestForRich:
    def __call__(self, acc):
        if acc.balance > 200000:
            return 0
        return acc.balance * 0.02