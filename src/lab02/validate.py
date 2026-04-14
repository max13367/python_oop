def ensure_string(value, field):
    if not isinstance(value, str):
        raise TypeError(f"{field} должно быть строкой")


def ensure_not_empty(value, field):
    if not value.strip():
        raise ValueError(f"{field} не может быть пустым")


def ensure_length(value, length, field):
    if len(value) != length:
        raise ValueError(f"{field} должен содержать {length} символов")


def ensure_positive_number(value, field):
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field} должно быть числом")
    if value < 0:
        raise ValueError(f"{field} не может быть меньше 0")


def ensure_currency(value):
    allowed = ["USD", "EUR", "RUB"]
    if value.upper() not in allowed:
        raise ValueError(f"Допустимые валюты: {allowed}")


# готовые проверки
def validate_account_id(value):
    ensure_string(value, "ID счета")
    ensure_length(value, 10, "ID счета")


def validate_owner_name(value):
    ensure_string(value, "Имя владельца")
    ensure_not_empty(value, "Имя владельца")


def validate_money(value, field):
    ensure_positive_number(value, field)