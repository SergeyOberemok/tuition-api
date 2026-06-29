from src.core.utils.id_generator import generate_question_id


def test_returns_a_non_empty_string():
    id_value = generate_question_id()

    assert isinstance(id_value, str)
    assert len(id_value) > 0


def test_generates_unique_values():
    assert generate_question_id() != generate_question_id()