#!/usr/bin/env python3
## Built from src\core\question_evaluation\question_evaluation.ipynb by nbtopy ##

# %%
from abc import abstractmethod

from src.core.assessment.assessment import IAssessmentItem
from src.core.strategies.question_adapter import IQuestionAdapter
from src.core.strategies.strategy_factory import StrategyFactory
from src.core.utils.id_generator import generate_question_id

# %%
class IQuestionEvaluation(IAssessmentItem):
    @abstractmethod
    def evaluate(self, answer) -> bool:
        pass

    @abstractmethod
    def goal(self):
        pass

# %%
class QuestionEvaluation(IQuestionEvaluation):
    def __init__(self, question, question_type, operation):
        self._id = generate_question_id()
        self._question = question
        self._type = question_type
        self._operation = operation
        self._answer = None
        self._is_correct = False
        self._is_answered = False

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def goal(self):
        return self._strategy().do_algorithm()

    @property
    def is_correct(self) -> bool:
        return self._is_correct

    @property
    def is_answered(self) -> bool:
        return self._is_answered

    def evaluate(self, answer) -> bool:
        self._answer = answer
        self._is_correct = self._strategy().compare(self._answer)
        self._is_answered = True

        return self._is_correct

    def _strategy(self):
        return StrategyFactory.create(type('Test', (IQuestionAdapter,), {
            'data': self._question,
            'type': self._type,
            'operation': self._operation
        })())

    def __str__(self):
        return str(self._strategy())
