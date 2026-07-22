from random import shuffle

from src.core.strategies.sequence_strategies import OrderedStrategy


def test_ordered_strategy():
    sequence_a = [1, 2, 3]
    sequence_b = sequence_a.copy()

    assert OrderedStrategy(sequence_a).compare(sequence_a) == True

    shuffle(sequence_b)

    assert OrderedStrategy(sequence_a, ).compare(sequence_b) == False
