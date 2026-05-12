from abc import ABC, abstractmethod
from typing import Any


class Printable(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass


class Processable(ABC):
    @abstractmethod
    def process(self):
        pass


class Withdrawable(ABC):
    @abstractmethod
    def withdraw_funds(self, amount: float):
        pass


class Comparable(ABC):
    @abstractmethod
    def compare_to(self, other: Any) -> int:
        pass