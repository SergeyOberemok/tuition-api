import pytest

from src.core.question_evaluation.question_evaluation import QuestionEvaluation
from src.core.question_evaluation.question_type import QuestionType
from src.core.strategies.calculation_strategies import CalculationType
from src.core.strategies.quiz_strategies import QuizType
from src.core.strategies.sequence_strategies import SequenceType


def test_type_returns_question_type():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    assert question_evaluation.type == QuestionType.CALCULATION


def test_is_correct_defaults_to_false():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    assert question_evaluation.is_correct == False


def test_goal_for_calculation_type():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    assert question_evaluation.goal == 5


def test_evaluate_with_correct_answer():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    result = question_evaluation.evaluate(5)

    assert result == True
    assert question_evaluation.is_correct == True


def test_evaluate_with_incorrect_answer():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    result = question_evaluation.evaluate(4)

    assert result == False
    assert question_evaluation.is_correct == False


def test_evaluate_overwrites_previous_result():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    question_evaluation.evaluate(5)
    assert question_evaluation.is_correct == True

    question_evaluation.evaluate(4)
    assert question_evaluation.is_correct == False


def test_str_for_calculation_type():
    question_evaluation = QuestionEvaluation([2, 3], QuestionType.CALCULATION, CalculationType.ADDITION)

    assert str(question_evaluation) == '2 + 3'


def test_evaluate_for_quiz_type():
    question_evaluation = QuestionEvaluation({'question': 1}, QuestionType.QUIZ, QuizType.FLASHCARD)

    assert question_evaluation.evaluate({'answer': 1}) == True
    assert question_evaluation.is_correct == True

    question_evaluation.evaluate({'answer': 2})
    assert question_evaluation.is_correct == False


def test_evaluate_for_sequence_type():
    question_evaluation = QuestionEvaluation(['a', 'b', 'c'], QuestionType.SEQUENCE, SequenceType.ORDERED)

    assert question_evaluation.evaluate(['a', 'b', 'c']) == True
    assert question_evaluation.is_correct == True

    question_evaluation.evaluate(['c', 'b', 'a'])
    assert question_evaluation.is_correct == False


def test_goal_raises_for_quiz_type():
    question_evaluation = QuestionEvaluation({'question': 1}, QuestionType.QUIZ, QuizType.FLASHCARD)

    with pytest.raises(TypeError):
        _ = question_evaluation.goal
