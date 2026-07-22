#!/usr/bin/env python3
## Built from src\core\strategies\quiz_strategies.ipynb by nbtopy ##

# %%
from abc import abstractmethod
from collections.abc import Callable
from enum import Enum

from src.core.strategies.strategy import IStrategy

# %%
class IQuizStrategy(IStrategy):
    def __init__(self, question):
        self._question = question

    @abstractmethod
    def do_algorithm(self, answer):
        pass

# %%
class QuizType(str, Enum):
    EQUALITY = 'equality'
    FLASHCARD = 'flashcard'

# %%
class EqualityStrategy(IQuizStrategy):
    def __init__(self, question, comparator: Callable[[any, any], bool] | None = None):
        super().__init__(question)
        self._comparator = comparator

    def do_algorithm(self, answer) -> bool:
        return self._comparator(self._question, answer) if self._comparator is not None else self._question == answer

    def compare(self, answer) -> bool:
        return self.do_algorithm(answer)

# %%
class FlashCardStrategy(EqualityStrategy, IQuizStrategy):
    def __init__(self, question):
        super().__init__(question, lambda a, b: a['question'] == b['answer'])

    def do_algorithm(self, answer) -> bool:
        return super().do_algorithm(answer)
