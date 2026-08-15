from flask import request
from flask_socketio import SocketIO, emit

from src.controllers.assessment_session_store import AssessmentSessionStore
from src.core.assessment.assessment_factory import AssessmentFactory
from src.core.utils.number_utils import generate_random_numbers_pairs

socketio = SocketIO(cors_allowed_origins='*', logger=True)
sessions = AssessmentSessionStore()


@socketio.on('start')
def handle_start(quantity: int):
    numbers_pairs = generate_random_numbers_pairs(max_number=10, count=quantity)

    assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)
    sessions.update(request.sid, assessment=assessment, assessment_iterator=iter(assessment))


@socketio.on('question')
def handle_question(args):
    session = sessions.get(request.sid)

    try:
        session.assessment_item = next(session.assessment_iterator)
        response = session.assessment_item.to_dict()

        return response
    except StopIteration:
        emit('end', {'assessment': 'end'})
        return ''


@socketio.on('answer')
def handle_answer(answer: str):
    session = sessions.get(request.sid)

    result = session.assessment_item.evaluate(answer)

    return result


@socketio.on('disconnect')
def handle_disconnect():
    sessions.reset(request.sid)
