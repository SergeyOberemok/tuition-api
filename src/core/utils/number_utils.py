import random
from collections.abc import Generator, Sequence


def generate_random_numbers(max_number: int, count: int) -> Generator[int, None, None]:
    numbers = [*range(1, max_number)]

    for _ in range(count):
        yield random.choice(numbers)


def generate_random_numbers_pairs(max_number: int, count: int) -> Sequence[Sequence[int]]:
    numbers_pairs = zip(
        generate_random_numbers(max_number, count),
        generate_random_numbers(max_number, count),
    )

    return [*numbers_pairs]
