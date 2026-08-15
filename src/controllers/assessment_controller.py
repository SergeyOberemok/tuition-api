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
    sessions.update(request.sid, assessment=assessment, assessment_item=None)


@socketio.on('question')
def handle_question(args=None):
    session = sessions.get(request.sid)

    if session.assessment is None:
        emit('error', {'message': 'Assessment not started'})
        return ''

    direction = (args or {}).get('direction', 'next')
    item = session.assessment.prev() if direction == 'prev' else session.assessment.next()

    if item is None:
        emit('end', {'assessment': 'end'})
        return ''

    session.assessment_item = item

    return item.to_dict()


@socketio.on('answer')
def handle_answer(answer: str):
    session = sessions.get(request.sid)

    if session.assessment_item is None:
        emit('error', {'message': 'No active question to answer'})
        return ''

    result = session.assessment_item.evaluate(answer)

    return result


@socketio.on('goal')
def handle_goal():
    session = sessions.get(request.sid)

    if session.assessment_item is None:
        emit('error', {'message': 'No active question to answer'})
        return ''

    return session.assessment_item.goal()


@socketio.on('disconnect')
def handle_disconnect():
    sessions.reset(request.sid)
