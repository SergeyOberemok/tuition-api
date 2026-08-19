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
    @abstractmethod
    def next(self) -> IAssessmentItem | None:
        pass

    @abstractmethod
    def prev(self) -> IAssessmentItem | None:
        pass

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
        self._index = -1

    def __iter__(self):
        self._index = -1
        return self

    def __next__(self):
        item = self.next()
        if item is None:
            raise StopIteration
        return item

    def next(self) -> IAssessmentItem | None:
        if self._index + 1 >= len(self._questions):
            return None

        self._index += 1
        return self._questions[self._index]

    def prev(self) -> IAssessmentItem | None:
        if not self._questions:
            return None

        self._index = max(self._index - 1, 0)
        return self._questions[self._index]

    @property
    def results(self) -> list[bool]:
        return [question.is_correct for question in self._questions]

    @property
    def result(self) -> bool:
        return all(self.results)

    def __str__(self):
        return '; '.join([str(q) for q in self._questions])
