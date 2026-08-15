#!/usr/bin/env python3
## Built from src\core\question_evaluation\question_evaluation.ipynb by nbtopy ##

# %%
from abc import abstractmethod

from src.core.assessment.assessment import IAssessmentItem
from src.core.strategies.question_adapter import IQuestionAdapter
from src.core.strategies.strategy_factory import StrategyFactory

# %%
class IQuestionEvaluation(IAssessmentItem):
    @abstractmethod
    def evaluate(self, answer) -> bool:
        pass

    @abstractmethod
    def goal(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

# %%
class QuestionEvaluation(IQuestionEvaluation):
    def __init__(self, question, question_type, operation):
        self._question = question
        self._type = question_type
        self._operation = operation
        self._answer = None
        self._is_correct = False

    @property
    def is_correct(self) -> bool:
        return self._is_correct

    def evaluate(self, answer) -> bool:
        self._answer = answer
        self._is_correct = self._strategy().compare(self._answer)

        return self._is_correct

    def goal(self):
        return self._strategy().do_algorithm()

    def _strategy(self):
        return StrategyFactory.create(type('Test', (IQuestionAdapter,), self.to_dict())())

    def to_dict(self) -> dict:
        return {
            'data': self._question,
            'type': self._type,
            'operation': self._operation
        }
