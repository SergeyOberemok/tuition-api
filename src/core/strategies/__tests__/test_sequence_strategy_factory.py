import pytest

from src.core.strategies.sequence_strategies import OrderedStrategy, SequenceType
from src.core.strategies.sequence_strategy_factory import SequenceStrategyFactory


def test_create_returns_ordered_strategy():
    result = SequenceStrategyFactory.create('ordered', [1, 2, 3])

    assert isinstance(result, OrderedStrategy)
    assert str(result) == '1 -> 2 -> 3'


def test_create_returns_ordered_strategy_for_ordered_type():
    result = SequenceStrategyFactory.create(SequenceType.ORDERED, [1, 2, 3])

    assert isinstance(result, OrderedStrategy)
    assert str(result) == '1 -> 2 -> 3'


def test_create_raises_for_unsupported_operation():
    with pytest.raises(NotImplementedError):
        SequenceStrategyFactory.create('unsupported', [1, 2, 3])
