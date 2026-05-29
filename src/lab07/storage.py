import json
from typing import List
from lab01.model import ClientAccount
from lab03.model import CreditAccount, SavingsAccount


def save(collection: List[ClientAccount], filepath: str) -> None:
    """Сохранить список счётов в JSON-файл.

    Args:
        collection: список объектов ClientAccount и его наследников.
        filepath: путь к файлу.
    """
    data = [acc.to_dict() for acc in collection]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(filepath: str) -> List[ClientAccount]:
    """Загрузить список счётов из JSON-файла.

    Если файл не найден — вернуть пустой список.

    Args:
        filepath: путь к файлу.

    Returns:
        Список восстановленных объектов.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []

    result: List[ClientAccount] = []
    for item in data:
        acc_type = item.get("type", "standard")
        if acc_type == "credit":
            result.append(CreditAccount.from_dict(item))
        elif acc_type == "savings":
            result.append(SavingsAccount.from_dict(item))
        else:
            result.append(ClientAccount.from_dict(item))
    return result