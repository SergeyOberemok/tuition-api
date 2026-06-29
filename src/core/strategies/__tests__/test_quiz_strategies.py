from src.core.strategies.quiz_strategies import EqualityStrategy, FlashCardStrategy


def test_equality_strategy():
    assert EqualityStrategy(1).do_algorithm(1) == True
    assert EqualityStrategy(1).do_algorithm(2) == False


def test_equality_strategy_compare():
    assert EqualityStrategy(1).compare(1) == True
    assert EqualityStrategy(1).compare(2) == False


def test_equality_strategy_with_custom_comparator():
    comparator = lambda question, answer: question.lower() == answer.lower()

    strategy = EqualityStrategy('Hello', comparator)

    assert strategy.do_algorithm('hello') == True
    assert strategy.do_algorithm('world') == False


def test_equality_strategy_str():
    assert str(EqualityStrategy('question')) == 'question'


def test_flash_card_strategy():
    assert FlashCardStrategy({'question': 1}).do_algorithm({'answer': 1}) == True
    assert FlashCardStrategy({'question': 1}).do_algorithm({'answer': 2}) == False


def test_flash_card_strategy_compare():
    assert FlashCardStrategy({'question': 1}).compare({'answer': 1}) == True
    assert FlashCardStrategy({'question': 1}).compare({'answer': 2}) == False


def test_flash_card_strategy_str():
    assert str(FlashCardStrategy({'question': 1})) == str({'question': 1})
