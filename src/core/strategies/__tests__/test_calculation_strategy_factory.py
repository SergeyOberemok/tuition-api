import pytest

from src.core.strategies.calculation_strategies import AdditionStrategy, SubtractionStrategy, \
    MultiplicationStrategy, DivisionStrategy, CalculationType
from src.core.strategies.calculation_strategy_factory import CalculationStrategyFactory


def test_create_addition_strategy():
    result = CalculationStrategyFactory.create(CalculationType.ADDITION, [1, 2])

    assert isinstance(result, AdditionStrategy)
    assert str(result) == '1 + 2'


def test_create_subtraction_strategy():
    result = CalculationStrategyFactory.create(CalculationType.SUBTRACTION, [3, 2])

    assert isinstance(result, SubtractionStrategy)
    assert str(result) == '3 - 2'


def test_create_multiplication_strategy():
    result = CalculationStrategyFactory.create(CalculationType.MULTIPLICATION, [2, 3])

    assert isinstance(result, MultiplicationStrategy)
    assert str(result) == '2 x 3'


def test_create_division_strategy():
    result = CalculationStrategyFactory.create(CalculationType.DIVISION, [6, 2])

    assert isinstance(result, DivisionStrategy)
    assert str(result) == '6 / 2'


def test_create_raises_for_unsupported_operation():
    with pytest.raises(ValueError):
        CalculationStrategyFactory.create('%', [1, 2])


def test_create_addition_strategy_static_helper():
    result = CalculationStrategyFactory.create_addition_strategy([1, 2])

    assert isinstance(result, AdditionStrategy)
    assert str(result) == '1 + 2'


def test_create_subtraction_strategy_static_helper():
    result = CalculationStrategyFactory.create_subtraction_strategy([3, 2])

    assert isinstance(result, SubtractionStrategy)
    assert str(result) == '3 - 2'


def test_create_multiplication_strategy_static_helper():
    result = CalculationStrategyFactory.create_multiplication_strategy([2, 3])

    assert isinstance(result, MultiplicationStrategy)
    assert str(result) == '2 x 3'


def test_create_division_strategy_static_helper():
    result = CalculationStrategyFactory.create_division_strategy([6, 2])

    assert isinstance(result, DivisionStrategy)
    assert str(result) == '6 / 2'
