import pytest

from src.core.strategies.quiz_strategies import EqualityStrategy, FlashCardStrategy, QuizType
from src.core.strategies.quiz_strategy_factory import QuizStrategyFactory


def test_create_equality_strategy():
    result = QuizStrategyFactory.create(QuizType.EQUALITY, 1)

    assert isinstance(result, EqualityStrategy)
    assert not isinstance(result, FlashCardStrategy)


def test_create_flashcard_strategy():
    result = QuizStrategyFactory.create(QuizType.FLASHCARD, {'question': 1})

    assert isinstance(result, FlashCardStrategy)


def test_create_raises_for_unsupported_operation():
    with pytest.raises(NotImplementedError):
        QuizStrategyFactory.create('unsupported', {})
