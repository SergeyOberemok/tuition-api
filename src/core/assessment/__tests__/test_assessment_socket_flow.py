from src.controllers.assessment_session_store import AssessmentSessionStore
from src.core.assessment.assessment_factory import AssessmentFactory


class TestAssessmentSocketHandlerFlow:
    def test_matches_controller_socket_handlers(self):
        sessions = AssessmentSessionStore()
        sid = 'test-sid'

        # 'start': build the assessment from number pairs and store it on the session
        numbers_pairs = [(2, 3), (5, 1), (4, 4)]
        assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)
        sessions.update(sid, assessment=assessment, assessment_item=None)

        for index, (a, b) in enumerate(numbers_pairs):
            # 'question' (direction='next'): advance the iterator and remember the current item
            session = sessions.get(sid)
            item = session.assessment.next()
            assert item is not None
            session.assessment_item = item

            # handle_question returns {'id': item.id, 'question': str(item), 'type': item.type}
            assert str(item) == f'{a} + {b}'

            # 'goal': read the target answer for the current question
            assert session.assessment_item.goal == a + b

            # 'answer': evaluate the current question; handle_answer emits 'end' once every
            # item is answered - i.e. only after the last pair in this loop
            result = session.assessment_item.evaluate(a + b)
            assert result == True
            assert session.assessment.is_complete == (index == len(numbers_pairs) - 1)

        assert session.assessment.result == True

        # handle_answer's 'end' emit is built from session.assessment.get_summary()
        end_payload = session.assessment.get_summary()
        assert [entry['question'] for entry in end_payload] == [f'{a} + {b}' for a, b in numbers_pairs]
        assert [entry['result'] for entry in end_payload] == [True, True, True]
        assert len({entry['id'] for entry in end_payload}) == len(numbers_pairs)

        # 'question' (direction='prev') still works after completion, to review a past question
        session = sessions.get(sid)
        item = session.assessment.prev()
        assert item is not None
        session.assessment_item = item
        assert session.assessment_item.is_correct == True

        # 'question' (direction='next') after completion returns None; handle_question emits an error
        session.assessment.next()
        assert session.assessment.next() is None

        # 'disconnect': the session is discarded
        sessions.reset(sid)
        assert sessions.get(sid).assessment is None

    def test_reports_incorrect_answers(self):
        sessions = AssessmentSessionStore()
        sid = 'test-sid'

        numbers_pairs = [(2, 3), (5, 1)]
        assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)
        sessions.update(sid, assessment=assessment, assessment_item=None)

        session = sessions.get(sid)

        item = session.assessment.next()
        session.assessment_item = item
        assert str(item) == '2 + 3'
        assert session.assessment_item.evaluate(5) == True

        item = session.assessment.next()
        session.assessment_item = item
        assert str(item) == '5 + 1'
        assert session.assessment_item.evaluate(0) == False

        assert session.assessment.results == [True, False]
        assert session.assessment.result == False
        assert str(session.assessment) == '2 + 3; 5 + 1'

    def test_reaching_the_end_loops_to_first_unanswered_instead_of_ending(self):
        sessions = AssessmentSessionStore()
        sid = 'test-sid'

        numbers_pairs = [(2, 3), (5, 1), (4, 4)]
        assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)
        sessions.update(sid, assessment=assessment, assessment_item=None)
        session = sessions.get(sid)

        # walk through all three questions, but leave the middle one unanswered
        first = session.assessment.next()
        second = session.assessment.next()
        third = session.assessment.next()

        first.evaluate(5)
        third.evaluate(8)

        # 'question' (direction='next') at the end, with an unanswered item remaining, loops back to it
        looped_item = session.assessment.next()
        assert looped_item is second

        second.evaluate(6)

        # advance back to the last item, then confirm the assessment now truly ends
        session.assessment.next()
        assert session.assessment.next() is None
