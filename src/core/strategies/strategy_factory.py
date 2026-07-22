from src.core.question_evaluation.question_type import QuestionType
from src.core.strategies.calculation_strategy_factory import CalculationStrategyFactory
from src.core.strategies.question_adapter import IQuestionAdapter
from src.core.strategies.quiz_strategy_factory import QuizStrategyFactory
from src.core.strategies.sequence_strategy_factory import SequenceStrategyFactory
from src.core.strategies.strategy import IStrategy


class StrategyFactory:
    @staticmethod
    def create(question: IQuestionAdapter) -> IStrategy:
        match question.type:
            case QuestionType.CALCULATION:
                return CalculationStrategyFactory.create(question.operation, question.data)
            case QuestionType.SEQUENCE:
                return SequenceStrategyFactory.create(question.operation, question.data)
            case QuestionType.QUIZ:
                return QuizStrategyFactory.create(question.operation, question.data)
            case _:
                raise NotImplementedError
