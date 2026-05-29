class AccountNotFoundError(Exception):
    """Счёт с указанным ID не найден в коллекции."""
    pass


class DuplicateAccountError(Exception):
    """Счёт с таким ID уже существует в коллекции."""
    pass


class AccountBlockedError(Exception):
    """Операция невозможна: счёт заблокирован."""
    pass


class InsufficientFundsError(Exception):
    """Недостаточно средств для выполнения операции."""
    pass