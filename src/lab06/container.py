from typing import TypeVar, Generic, Callable, Optional, Protocol, runtime_checkable

#  Протоколы (структурная типизация)

@runtime_checkable
class Displayable(Protocol):
    """
    Протокол: объект должен уметь возвращать
    строковое представление через display().
    Явного наследования не требуется — достаточно
    наличия метода с нужной сигнатурой.
    """
    def display(self) -> str:
        ...


@runtime_checkable
class Scorable(Protocol):
    """
    Протокол: объект должен уметь возвращать
    числовую оценку через score().
    """
    def score(self) -> float:
        ...

#  TypeVar-ы

T = TypeVar('T')                      # произвольный тип элемента
R = TypeVar('R')                      # тип результата map()
D = TypeVar('D', bound=Displayable)   # только Displayable-совместимые
S = TypeVar('S', bound=Scorable)      # только Scorable-совместимые


#  Обобщённая коллекция

class TypedCollection(Generic[T]):
    """
    Типизированная Generic-коллекция.

    Параметр T фиксируется при создании:
        col: TypedCollection[ClientAccount] = TypedCollection()

    Все методы из AccountStorage (ЛР-2) перенесены сюда
    с корректными аннотациями типов.
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    # ── базовые операции ─────────────────────

    def append(self, item: T) -> None:
        """Добавить элемент в конец коллекции."""
        self._items.append(item)

    def delete(self, item: T) -> None:
        """Удалить первое вхождение элемента."""
        if item in self._items:
            self._items.remove(item)

    def delete_by_index(self, idx: int) -> None:
        """Удалить элемент по индексу."""
        if idx < 0 or idx >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        self._items.pop(idx)

    def all(self) -> list[T]:
        """Вернуть копию внутреннего списка."""
        return list(self._items)

    def clear(self) -> None:
        """Очистить коллекцию."""
        self._items.clear()

    # сортировка

    def sort_by(self, key_func: Callable[[T], any]) -> None:
        """Сортировать по произвольному ключу."""
        self._items.sort(key=key_func)

    # протокол последовательности

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item: object) -> bool:
        return item in self._items

    # функциональные методы

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Найти первый элемент, для которого predicate → True.
        Если не найден — вернуть None.
        """
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """
        Вернуть список элементов, удовлетворяющих условию.
        Исходная коллекция не меняется.
        """
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        """
        Применить функцию к каждому элементу.
        Возвращает list[R] — тип результата может отличаться от T.
        Для этого введён отдельный TypeVar R.
        """
        return [transform(item) for item in self._items]

    # строковое представление

    def __str__(self) -> str:
        if not self._items:
            return "TypedCollection (пусто)"
        lines = "\n  ".join(str(item) for item in self._items)
        return f"TypedCollection [{len(self._items)} эл.]:\n  {lines}"

    def __repr__(self) -> str:
        return f"TypedCollection(items={self._items!r})"