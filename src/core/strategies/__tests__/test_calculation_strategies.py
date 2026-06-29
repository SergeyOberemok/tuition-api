from src.core.strategies.calculation_strategies import AdditionStrategy, SubtractionStrategy, MultiplicationStrategy, \
    DivisionStrategy


def test_addition_strategy():
    numbers = [1, 2]

    strategy = AdditionStrategy(numbers)

    assert strategy.do_algorithm() == 3
    assert strategy.compare(3) == True
    assert strategy.compare(4) == False
    assert str(strategy) == ' + '.join(map(str, numbers))


def test_addition_strategy_with_more_than_two_numbers():
    numbers = [1, 2, 3, 4]

    strategy = AdditionStrategy(numbers)

    assert strategy.do_algorithm() == 10
    assert strategy.compare(10) == True


def test_substraction_strategy():
    numbers = (3, 2)

    strategy = SubtractionStrategy(numbers)

    assert strategy.do_algorithm() == 1
    assert strategy.compare(1) == True
    assert strategy.compare(0) == False
    assert str(strategy) == ' - '.join(map(str, numbers))


def test_substraction_strategy_applies_numbers_in_order():
    numbers = (10, 2, 3)

    strategy = SubtractionStrategy(numbers)

    assert strategy.do_algorithm() == 5


def test_multiplication_strategy():
    numbers = [2, 3]

    strategy = MultiplicationStrategy(numbers)

    assert strategy.do_algorithm() == 6
    assert strategy.compare(6) == True
    assert strategy.compare(5) == False
    assert str(strategy) == ' x '.join(map(str, numbers))


def test_multiplication_strategy_with_more_than_two_numbers():
    numbers = [2, 3, 4]

    strategy = MultiplicationStrategy(numbers)

    assert strategy.do_algorithm() == 24


def test_division_strategy():
    numbers = (6, 2)

    strategy = DivisionStrategy(numbers)

    assert strategy.do_algorithm() == 3
    assert strategy.compare(3) == True
    assert strategy.compare(2) == False
    assert str(strategy) == ' / '.join(map(str, numbers))


def test_division_strategy_applies_numbers_in_order():
    numbers = (100, 2, 5)

    strategy = DivisionStrategy(numbers)

    assert strategy.do_algorithm() == 10
