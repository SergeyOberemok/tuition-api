import pytest

from src.core.strategies.sequence_strategies import OrderedStrategy


def test_ordered_strategy():
    sequence_a = [1, 2, 3]
    sequence_b = [3, 1, 2]

    assert OrderedStrategy(sequence_a).compare(sequence_a) == True
    assert OrderedStrategy(sequence_a).compare(sequence_b) == False


def test_ordered_strategy_do_algorithm_returns_elementwise_comparison():
    sequence_a = [1, 2, 3]

    strategy = OrderedStrategy(sequence_a)

    assert strategy.do_algorithm([1, 5, 3]) == [True, False, True]


def test_ordered_strategy_with_custom_comparator():
    comparator = lambda a, b: a.lower() == b.lower()

    strategy = OrderedStrategy(['A', 'B'], comparator)

    assert strategy.compare(['a', 'b']) == True
    assert strategy.compare(['a', 'c']) == False


def test_ordered_strategy_raises_for_empty_sequence():
    with pytest.raises(ValueError):
        OrderedStrategy([])


def test_ordered_strategy_raises_when_lengths_differ():
    strategy = OrderedStrategy([1, 2, 3])

    with pytest.raises(ValueError):
        strategy.do_algorithm([1, 2])


def test_ordered_strategy_str():
    sequence = [1, 2, 3]

    assert str(OrderedStrategy(sequence)) == ' -> '.join(map(str, sequence))
