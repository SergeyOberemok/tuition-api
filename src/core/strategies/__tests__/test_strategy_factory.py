import pytest

from src.core.question_evaluation.question_type import QuestionType
from src.core.strategies.calculation_strategies import CalculationType, ICalculationStrategy, AdditionStrategy
from src.core.strategies.question_adapter import IQuestionAdapter
from src.core.strategies.quiz_strategies import QuizType, IQuizStrategy, FlashCardStrategy, EqualityStrategy
from src.core.strategies.sequence_strategies import ISequenceStrategy, OrderedStrategy
from src.core.strategies.strategy_factory import StrategyFactory


def test_calculation_strategy_factory():
    question = type('Test', (IQuestionAdapter,), {
        'type': QuestionType.CALCULATION,
        'data': [1, 2, 3],
        'operation': CalculationType.ADDITION
    })()

    result = StrategyFactory.create(question)

    assert isinstance(result, ICalculationStrategy)
    assert isinstance(result, AdditionStrategy)


def test_sequence_strategy_factory():
    question = type('Test', (IQuestionAdapter,), {
        'type': QuestionType.SEQUENCE,
        'data': [1, 2, 3],
        'operation': 'ordered'
    })()

    result = StrategyFactory.create(question)

    assert isinstance(result, ISequenceStrategy)
    assert isinstance(result, OrderedStrategy)


def test_quiz_strategy_factory():
    question = type('Test', (IQuestionAdapter,), {
        'type': QuestionType.QUIZ,
        'data': {'question': 1},
        'operation': QuizType.FLASHCARD
    })()

    result = StrategyFactory.create(question)

    assert isinstance(result, IQuizStrategy)
    assert isinstance(result, FlashCardStrategy)


def test_quiz_strategy_factory_equality():
    question = type('Test', (IQuestionAdapter,), {
        'type': QuestionType.QUIZ,
        'data': 1,
        'operation': QuizType.EQUALITY
    })()

    result = StrategyFactory.create(question)

    assert isinstance(result, IQuizStrategy)
    assert isinstance(result, EqualityStrategy)


def test_strategy_factory_raises_for_unsupported_question_type():
    question = type('Test', (IQuestionAdapter,), {
        'type': 'unsupported',
        'data': None,
        'operation': None
    })()

    with pytest.raises(NotImplementedError):
        StrategyFactory.create(question)
