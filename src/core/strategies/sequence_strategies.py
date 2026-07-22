#!/usr/bin/env python3
## Built from src\core\strategies\sequence_strategies.ipynb by nbtopy ##

# %%
from abc import abstractmethod
from collections.abc import Sequence, Callable

from src.core.strategies.strategy import IStrategy

# %%
class ISequenceStrategy(IStrategy[Sequence]):
    def __init__(self, sequence: Sequence):
        if len(sequence) == 0:
            raise ValueError('Sequence must not be empty')

        self._sequence = sequence

    @abstractmethod
    def do_algorithm(self, sequence: Sequence) -> Sequence:
        pass

    def __str__(self) -> str:
        return ' -> '.join(map(str, self._sequence))

# %%
class OrderedStrategy(ISequenceStrategy):
    def __init__(self, sequence: Sequence, comparator: Callable[[any, any], bool] | None = None):
        super().__init__(sequence)
        self._comparator = comparator

    def do_algorithm(self, sequence: Sequence) -> Sequence:
        if len(self._sequence) != len(sequence):
            raise ValueError('Sequences must be of the same length')

        def comparator(a, b) -> bool:
            return self._comparator(a, b) if self._comparator is not None else a == b

        result = [comparator(a, b) for a, b in zip(self._sequence, sequence)]

        return result

    def compare(self, sequence: Sequence) -> bool:
        return all(self.do_algorithm(sequence))
