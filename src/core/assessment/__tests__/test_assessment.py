from src.core.assessment.assessment import Assessment
from src.core.assessment.assessment_factory import AssessmentFactory


def _addition_assessment(numbers_pairs):
    return AssessmentFactory.create_addition_assessment(numbers_pairs)


class TestNext:
    def test_returns_items_in_order_then_loops_to_first_unanswered(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])

        goals = [assessment.next().goal, assessment.next().goal, assessment.next().goal]

        assert goals == [2, 4, 6]
        assert assessment.next().goal == 2

    def test_returns_none_once_all_items_answered(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])
        items = [assessment.next() for _ in range(3)]

        for item in items:
            item.evaluate(item.goal)

        assert assessment.next() is None

    def test_loops_to_first_unanswered_skipping_answered_ones(self):
        assessment = _addition_assessment([(1, 1), (2, 2), (3, 3)])
        items = [assessment.next() for _ in range(3)]

        items[0].evaluate(items[0].goal)
        items[2].evaluate(items[2].goal)

        assert assessment.next().goal == 4

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
        assert assessment.next().goal == 2


class TestItems:
    def test_returns_underlying_questions(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])

        assert [item.goal for item in assessment.items] == [2, 4]


class TestIsComplete:
    def test_false_while_any_item_unanswered(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])
        items = list(assessment)

        items[0].evaluate(2)

        assert assessment.is_complete == False

    def test_true_once_every_item_answered(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])
        items = list(assessment)

        items[0].evaluate(2)
        items[1].evaluate(0)

        assert assessment.is_complete == True

    def test_true_for_empty_assessment(self):
        assessment = Assessment([])

        assert assessment.is_complete == True


class TestGetSummary:
    def test_returns_id_question_and_result_per_item(self):
        assessment = _addition_assessment([(1, 1), (2, 2)])
        items = list(assessment)

        items[0].evaluate(2)
        items[1].evaluate(0)

        summary = assessment.get_summary()

        assert [entry['question'] for entry in summary] == ['1 + 1', '2 + 2']
        assert [entry['result'] for entry in summary] == [True, False]
        assert [entry['id'] for entry in summary] == [item.id for item in items]

    def test_empty_for_empty_assessment(self):
        assessment = Assessment([])

        assert assessment.get_summary() == []


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
