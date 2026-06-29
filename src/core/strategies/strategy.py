from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IStrategy(ABC, Generic[T]):
    @abstractmethod
    def do_algorithm(self, *args, **kwargs) -> T:
        pass

    @abstractmethod
    def compare(self, answer) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
