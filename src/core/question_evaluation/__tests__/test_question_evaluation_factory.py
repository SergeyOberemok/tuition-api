import pytest

from src.core.question_evaluation.question_evaluation_factory import QuestionEvaluationFactory

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
        'items': ['question', 'answer'],
        'operation': 'flashcard'
    }
]


@pytest.mark.parametrize('question, operation, answer', [(*list(questions[0].values()), 5)])
def test_question_evaluation_factory(question, operation, answer):
    question_evaluation = QuestionEvaluationFactory.create(question, operation)

    result = question_evaluation.evaluate(answer)

    assert isinstance(question_evaluation.to_dict(), dict)
    assert result == True
