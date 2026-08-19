from src.core.assessment.assessment import Assessment
from src.core.assessment.assessment_factory import AssessmentFactory


def _addition_assessment(numbers_pairs):
    return AssessmentFactory.create_addition_assessment(numbers_pairs)


class TestNext:
    def test_returns_items_in_order_then_none(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])

        goals = [assessment.next().goal, assessment.next().goal, assessment.next().goal]

        assert goals == [2, 4, 6]
        assert assessment.next() is None

    def test_on_empty_assessment_returns_none(self):
        assessment = Assessment([])

        assert assessment.next() is None


class TestPrev:
    def test_on_empty_assessment_returns_none(self):
        assessment = Assessment([])

        assert assessment.prev() is None

    def test_before_any_next_returns_first_item(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])

        assert assessment.prev().goal == 2

    def test_steps_backward_and_clamps_at_start(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])

        assessment.next()
        assessment.next()
        assessment.next()

        assert assessment.prev().goal == 4
        assert assessment.prev().goal == 2
        assert assessment.prev().goal == 2


class TestNavigation:
    def test_forward_and_backward_like_question_handler(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])

        assert assessment.next().goal == 2
        assert assessment.next().goal == 4
        assert assessment.prev().goal == 2
        assert assessment.next().goal == 4
        assert assessment.next().goal == 6
        assert assessment.next() is None


class TestIteration:
    def test_iter_resets_index_allowing_re_iteration(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])

        first_pass = [item.goal for item in assessment]
        second_pass = [item.goal for item in assessment]

        assert first_pass == second_pass == [2, 4]


class TestResults:
    def test_reflects_each_item_correctness(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])
        items = list(assessment)

        items[0].evaluate(2)
        items[1].evaluate(0)
        items[2].evaluate(6)

        assert assessment.results == [True, False, True]

    def test_result_false_when_any_item_incorrect(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])
        items = list(assessment)

        items[0].evaluate(2)
        items[1].evaluate(0)

        assert assessment.result == False

    def test_result_true_for_empty_assessment(self):
        assessment = Assessment([])

        assert assessment.result == True


class TestStr:
    def test_joins_item_strings_with_semicolon(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])

        assert str(assessment) == '1 + 1; 2 + 2; 3 + 3'

    def test_empty_for_empty_assessment(self):
        assessment = Assessment([])

        assert str(assessment) == ''
