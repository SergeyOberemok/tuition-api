from abc import ABC
from collections.abc import Iterable

from src.core.strategies.quiz_strategies import EqualityStrategy, FlashCardStrategy, QuizType


class QuizStrategyFactory(ABC):
    @staticmethod
    def create(operation: str, items: dict) -> EqualityStrategy | FlashCardStrategy:
        match operation:
            case QuizType.EQUALITY:
                return EqualityStrategy(items)
            case QuizType.FLASHCARD:
                return FlashCardStrategy(items)
            case _:
                raise NotImplementedError
