import pytest

from src.core.assessment.assessment_factory import AssessmentFactory

questions_test_data = [
    ([2, 3], '+', 5),
    ([2, 3], '-', -1),
    ([2, 3], '*', 6),
    ([2, 2], '/', 1)
]


@pytest.mark.parametrize('questions, answers', [([(question, answer) for question, answer, _ in questions_test_data],
                                                 [answer for *_, answer in questions_test_data])])
def test_assessment(questions, answers):
    assessment = AssessmentFactory.create(questions)

    for index, question in enumerate(assessment):
        result = question.evaluate(answers[index])

        assert result == True

    assert assessment.result == True
