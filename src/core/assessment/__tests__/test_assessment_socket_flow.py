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

        for a, b in numbers_pairs:
            # 'question' (direction='next'): advance the iterator and remember the current item
            session = sessions.get(sid)
            item = session.assessment.next()
            assert item is not None
            session.assessment_item = item

            # 'goal': read the target answer for the current question
            assert session.assessment_item.goal == a + b

            # 'answer': evaluate the current question
            result = session.assessment_item.evaluate(a + b)
            assert result == True

        # 'question' (direction='prev'): step back to the previous question
        session = sessions.get(sid)
        item = session.assessment.prev()
        assert item is not None
        session.assessment_item = item
        assert session.assessment_item.is_correct == True

        # 'question' (direction='next') beyond the last question emits 'end'
        session.assessment.next()
        end_item = session.assessment.next()
        assert end_item is None

        assert session.assessment.result == True

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
        assert session.assessment_item.evaluate(5) == True

        item = session.assessment.next()
        session.assessment_item = item
        assert session.assessment_item.evaluate(0) == False

        assert session.assessment.results == [True, False]
        assert session.assessment.result == False
