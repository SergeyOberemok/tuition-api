from abc import ABC

from src.core.question_evaluation.question_evaluation import IQuestionEvaluation, QuestionEvaluation
from src.core.question_evaluation.question_type import QuestionType
from src.core.strategies.calculation_strategies import CalculationType
from src.core.strategies.quiz_strategies import QuizType


class QuestionEvaluationFactory(ABC):
    @staticmethod
    def create(question, operation: str) -> IQuestionEvaluation:
        if operation in [e.value for e in CalculationType]:
            return QuestionEvaluationFactory.create_calculation_type_evaluation(question, operation)
        elif operation in [e.value for e in QuestionType]:
            return QuestionEvaluationFactory.create_sequence_type_evaluation(question, operation)
        elif operation in [e.value for e in QuizType]:
            return QuestionEvaluationFactory.create_quiz_type_evaluation(question, operation)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    @staticmethod
    def create_calculation_type_evaluation(question, operation) -> IQuestionEvaluation:
        return QuestionEvaluation(question, QuestionType.CALCULATION, CalculationType(operation))

    @staticmethod
    def create_sequence_type_evaluation(question, operation) -> IQuestionEvaluation:
        return QuestionEvaluation(question, QuestionType.SEQUENCE, operation)

    @staticmethod
    def create_quiz_type_evaluation(question, operation) -> IQuestionEvaluation:
        return QuestionEvaluation(question, QuestionType.QUIZ, QuizType(operation))
