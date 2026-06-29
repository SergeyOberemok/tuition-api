from abc import ABC
from collections.abc import Sequence
from numbers import Number

from src.core.strategies.calculation_strategies import ICalculationStrategy, CalculationType, AdditionStrategy, \
    MultiplicationStrategy, SubtractionStrategy, DivisionStrategy


class CalculationStrategyFactory(ABC):
    @staticmethod
    def create(operation: str, numbers: Sequence[Number]) -> ICalculationStrategy:
        match operation:
            case CalculationType.ADDITION:
                return CalculationStrategyFactory.create_addition_strategy(numbers)
            case CalculationType.SUBTRACTION:
                return CalculationStrategyFactory.create_subtraction_strategy(numbers)
            case CalculationType.MULTIPLICATION:
                return CalculationStrategyFactory.create_multiplication_strategy(numbers)
            case CalculationType.DIVISION:
                return CalculationStrategyFactory.create_division_strategy(numbers)
            case _:
                raise ValueError(f"Unsupported operation: {operation}")

    @staticmethod
    def create_addition_strategy(numbers: Sequence[Number]) -> ICalculationStrategy:
        return AdditionStrategy(numbers)

    @staticmethod
    def create_multiplication_strategy(numbers: Sequence[Number]) -> ICalculationStrategy:
        return MultiplicationStrategy(numbers)

    @staticmethod
    def create_subtraction_strategy(numbers: Sequence[Number]) -> ICalculationStrategy:
        return SubtractionStrategy(numbers)

    @staticmethod
    def create_division_strategy(numbers: Sequence[Number]) -> ICalculationStrategy:
        return DivisionStrategy(numbers)
