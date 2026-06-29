import pytest

from src.core.assessment.assessment import Assessment
from src.core.assessment.assessment_factory import AssessmentFactory
from src.core.question_evaluation.question_type import QuestionType

questions_test_data = [
    ([2, 3], '+', 5),
    ([2, 3], '-', -1),
    ([2, 3], '*', 6),
    ([2, 2], '/', 1)
]


@pytest.mark.parametrize('questions, answers', [([(question, answer) for question, answer, _ in questions_test_data],
                                                 [answer for *_, answer in questions_test_data])])
def test_create_with_calculation_questions(questions, answers):
    assessment = AssessmentFactory.create(questions)

    for index, question in enumerate(assessment):
        result = question.evaluate(answers[index])

        assert result == True

    assert assessment.result == True


def test_create_with_mixed_question_types():
    questions = [
        ([2, 3], '+'),
        (['a', 'b', 'c'], 'ordered'),
        ({'question': 1}, 'flashcard'),
    ]

    assessment = AssessmentFactory.create(questions)

    assert isinstance(assessment, Assessment)

    calculation, sequence, quiz = list(assessment)

    assert calculation.type == QuestionType.CALCULATION
    assert sequence.type == QuestionType.SEQUENCE
    assert quiz.type == QuestionType.QUIZ

    assert calculation.evaluate(5) == True
    assert sequence.evaluate(['a', 'b', 'c']) == True
    assert quiz.evaluate({'answer': 1}) == True

    assert str(calculation) == '2 + 3'
    assert str(sequence) == 'a -> b -> c'
    assert str(quiz) == str({'question': 1})
    assert str(assessment) == '2 + 3; a -> b -> c; ' + str({'question': 1})

    assert assessment.result == True


def test_create_raises_for_unsupported_operation():
    with pytest.raises(ValueError):
        AssessmentFactory.create([([1, 2], 'unsupported')])


def test_create_addition_assessment():
    numbers_pairs = [(2, 3), (5, 1), (4, 4)]

    assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)

    assert isinstance(assessment, Assessment)

    items = list(assessment)

    assert len(items) == len(numbers_pairs)
    assert all(item.type == QuestionType.CALCULATION for item in items)
    assert [item.goal for item in items] == [5, 6, 8]
    assert str(assessment) == '2 + 3; 5 + 1; 4 + 4'


def test_create_addition_assessment_evaluates_answers():
    numbers_pairs = [(2, 3), (5, 1)]

    assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)

    first, second = list(assessment)

    assert first.evaluate(5) == True
    assert second.evaluate(0) == False

    assert assessment.results == [True, False]
    assert assessment.result == False


def test_create_addition_assessment_with_no_questions():
    assessment = AssessmentFactory.create_addition_assessment([])

    assert list(assessment) == []
    assert assessment.result == True
