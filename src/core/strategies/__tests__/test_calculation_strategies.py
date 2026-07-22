from src.core.strategies.calculation_strategies import AdditionStrategy, SubtractionStrategy, MultiplicationStrategy, \
    DivisionStrategy


def test_addition_strategy():
    numbers = [1, 2]

    strategy = AdditionStrategy(numbers)

    assert strategy.do_algorithm() == 3
    assert strategy.compare(3) == True
    assert str(strategy) == ' + '.join(map(str, numbers))


def test_substraction_strategy():
    numbers = (3, 2)

    strategy = SubtractionStrategy(numbers)

    assert strategy.do_algorithm() == 1
    assert strategy.compare(1) == True
    assert str(strategy) == ' - '.join(map(str, numbers))


def test_multiplication_strategy():
    numbers = [2, 3]

    strategy = MultiplicationStrategy(numbers)

    assert strategy.do_algorithm() == 6
    assert strategy.compare(6) == True
    assert str(strategy) == ' x '.join(map(str, numbers))


def test_division_strategy():
    numbers = (6, 2)

    strategy = DivisionStrategy(numbers)

    assert strategy.do_algorithm() == 3
    assert strategy.compare(3) == True
    assert str(strategy) == ' / '.join(map(str, numbers))
