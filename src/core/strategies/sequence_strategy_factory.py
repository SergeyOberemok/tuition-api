from abc import ABC
from collections.abc import Sequence

from src.core.strategies.sequence_strategies import OrderedStrategy


class SequenceStrategyFactory(ABC):
    @staticmethod
    def create(operation: str, sequences: Sequence) -> OrderedStrategy:
        match operation:
            case _:
                return OrderedStrategy(sequences)
