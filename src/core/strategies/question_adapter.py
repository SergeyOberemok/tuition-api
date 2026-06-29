from abc import ABC, abstractmethod

from src.core.question_evaluation.question_type import QuestionType


class IQuestionAdapter(ABC):
    @property
    @abstractmethod
    def type(self) -> QuestionType:
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def operation(self) -> str:
        pass
