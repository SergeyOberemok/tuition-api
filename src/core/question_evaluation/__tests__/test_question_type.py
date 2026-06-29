from src.core.question_evaluation.question_type import QuestionType
import json


def test_question_type_to_json():
    result = json.dumps(QuestionType.CALCULATION.value)

    assert result.strip('"') == QuestionType.CALCULATION.value