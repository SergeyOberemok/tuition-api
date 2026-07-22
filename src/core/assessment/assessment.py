#!/usr/bin/env python3
## Built from src\core\assessment\assessment.ipynb by nbtopy ##

# %%
from abc import ABC, abstractmethod
from collections.abc import Sequence, Iterable

# %% [markdown]
# ---

# %%
class IAssessmentItem(ABC):
    @property
    @abstractmethod
    def is_correct(self) -> bool:
        pass

# %%
class IAssessment(ABC, Iterable[IAssessmentItem]):
    @property
    @abstractmethod
    def results(self) -> list[bool]:
        pass

    @property
    @abstractmethod
    def result(self) -> bool:
        pass

# %%
class Assessment:
    def __init__(self, questions: Sequence[IAssessmentItem]):
        self._questions = questions
        self._iterator = None

    def __iter__(self):
        self._iterator = iter(self._questions)
        return self

    def __next__(self):
        return next(self._iterator)

    @property
    def results(self) -> list[bool]:
        return [question.is_correct for question in self._questions]

    @property
    def result(self) -> bool:
        return all(self.results)
