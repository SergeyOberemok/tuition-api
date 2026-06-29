#!/usr/bin/env python3
## Built from src\core\strategies\calculation_strategies.ipynb by nbtopy ##

# %%
from abc import abstractmethod
from collections.abc import Sequence
from enum import Enum
from functools import reduce
from numbers import Number

from src.core.strategies.strategy import IStrategy

# %% [markdown]
# ---

# %%
class CalculationType(str, Enum):
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'

# %%
class ICalculationStrategy(IStrategy[Number]):
    def __init__(self, numbers: Sequence[Number]):
        self._numbers = numbers

    @abstractmethod
    def do_algorithm(self) -> Number:
        pass

    def compare(self, answer: Number) -> bool:
        return self.do_algorithm() == answer

    @property
    @abstractmethod
    def operation(self) -> str:
        pass

    def __str__(self) -> str:
        return f' {self.operation} '.join(map(str, self._numbers))

# %% [markdown]
# ##### Addition

# %%
class AdditionStrategy(ICalculationStrategy):
    def __init__(self, numbers: Sequence[Number]):
        super().__init__(numbers)

    def do_algorithm(self) -> Number:
        return sum(self._numbers)

    @property
    def operation(self) -> str:
        return '+'

# %% [markdown]
# ##### Subtraction

# %%
class SubtractionStrategy(ICalculationStrategy):
    def __init__(self, numbers: Sequence[Number]):
        super().__init__(numbers)
        self._operation = '-'

    def do_algorithm(self) -> Number:
        return reduce(lambda acc, number: acc - number, self._numbers)

    @property
    def operation(self):
        return self._operation

# %% [markdown]
# ##### Multiplication

# %%
class MultiplicationStrategy(ICalculationStrategy):
    def __init__(self, numbers: Sequence[Number]):
        super().__init__(numbers)
        self._operation = '*'

    def do_algorithm(self) -> Number:
        return reduce(lambda acc, number: acc * number, self._numbers)

    @property
    def operation(self) -> str:
        return 'x'

# %% [markdown]
# ##### Division

# %%
class DivisionStrategy(ICalculationStrategy):
    def __init__(self, numbers: Sequence[Number]):
        super().__init__(numbers)
        self._operation = '/'

    def do_algorithm(self) -> Number:
        return reduce(lambda acc, number: acc / number, self._numbers)

    @property
    def operation(self) -> str:
        return self._operation
