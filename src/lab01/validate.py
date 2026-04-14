def check_name(value):
    if not isinstance(value, str):
        raise TypeError("Имя должно быть строкой")
    if not value.strip():
        raise ValueError("Имя не может быть пустым")


def check_id(value):
    if not isinstance(value, str):
        raise TypeError("ID должен быть строкой")
    if len(value) != 10:
        raise ValueError("ID должен содержать 10 символов")


def check_currency(value):
    allowed = {"USD", "EUR", "RUB"}
    if value.upper() not in allowed:
        raise ValueError(f"Допустимые валюты: {allowed}")


def check_money(value, field):
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field} должно быть числом")
    if value < 0:
        raise ValueError(f"{field} не может быть отрицательным")