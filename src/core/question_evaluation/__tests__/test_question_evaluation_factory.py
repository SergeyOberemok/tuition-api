import pytest

from src.core.question_evaluation.question_evaluation_factory import QuestionEvaluationFactory
from src.core.question_evaluation.question_type import QuestionType

questions = [
    {
        'items': [2, 3],
        'operation': '+'
    },
    {
        'items': ['asdf', 'qwer', 'zxcv'],
        'operation': 'ordered'
    },
    {
        'items': {'question': 1},
        'operation': 'flashcard'
    }
]


@pytest.mark.parametrize('question, operation, answer', [(*list(questions[0].values()), 5)])
def test_question_evaluation_factory(question, operation, answer):
    question_evaluation = QuestionEvaluationFactory.create(question, operation)

    result = question_evaluation.evaluate(answer)

    assert result == True


def test_create_calculation_type_evaluation():
    question, operation = questions[0].values()

    question_evaluation = QuestionEvaluationFactory.create(question, operation)

    assert question_evaluation.type == QuestionType.CALCULATION
    assert question_evaluation.evaluate(4) == False
    assert str(question_evaluation) == '2 + 3'


def test_create_sequence_type_evaluation():
    question, operation = questions[1].values()

    question_evaluation = QuestionEvaluationFactory.create(question, operation)

    assert question_evaluation.type == QuestionType.SEQUENCE
    assert question_evaluation.evaluate(question) == True
    assert question_evaluation.evaluate(['zxcv', 'qwer', 'asdf']) == False
    assert str(question_evaluation) == 'asdf -> qwer -> zxcv'


def test_create_quiz_type_evaluation():
    question, operation = questions[2].values()

    question_evaluation = QuestionEvaluationFactory.create(question, operation)

    assert question_evaluation.type == QuestionType.QUIZ
    assert question_evaluation.evaluate({'answer': 1}) == True
    assert question_evaluation.evaluate({'answer': 2}) == False
    assert str(question_evaluation) == str({'question': 1})


def test_create_quiz_type_evaluation_equality():
    question_evaluation = QuestionEvaluationFactory.create(1, 'equality')

    assert question_evaluation.type == QuestionType.QUIZ
    assert question_evaluation.evaluate(1) == True
    assert question_evaluation.evaluate(2) == False
    assert str(question_evaluation) == '1'


def test_create_raises_for_unsupported_operation():
    with pytest.raises(ValueError):
        QuestionEvaluationFactory.create([1, 2], 'unsupported')


def test_create_generates_a_unique_id():
    question, operation = questions[0].values()

    question_evaluation = QuestionEvaluationFactory.create(question, operation)

    assert isinstance(question_evaluation.id, str)
    assert len(question_evaluation.id) > 0
