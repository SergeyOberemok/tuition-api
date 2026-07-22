from src.core.strategies.quiz_strategies import EqualityStrategy, FlashCardStrategy


def test_equality_strategy():
    assert EqualityStrategy(1).do_algorithm(1) == True
    assert EqualityStrategy(1).do_algorithm(2) == False

def test_flash_card_strategy():
    assert FlashCardStrategy({'question': 1}).do_algorithm({'answer': 1}) == True
    assert FlashCardStrategy({'question': 1}).do_algorithm({'answer': 2}) == False
