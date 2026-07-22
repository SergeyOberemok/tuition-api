from collections.abc import Iterator

from flask_socketio import SocketIO, emit

from src.core.assessment.assessment import IAssessmentItem, IAssessment
from src.core.assessment.assessment_factory import AssessmentFactory
from src.core.question_evaluation.question_evaluation import IQuestionEvaluation
from src.core.utils.number_utils import generate_random_numbers_pairs

socketio = SocketIO(cors_allowed_origins='*', logger=True)
assessment: IAssessment | None = None
assessment_iterator: Iterator[IAssessmentItem] | None = None
assessment_item: IQuestionEvaluation | None = None


@socketio.on('start')
def handle_start(quantity: int):
    global assessment, assessment_iterator
    numbers_pairs = generate_random_numbers_pairs(max_number=10, count=quantity)

    assessment = AssessmentFactory.create_addition_assessment(numbers_pairs)
    assessment_iterator = iter(assessment)


@socketio.on('question')
def handle_question(args):
    global assessment_iterator, assessment_item

    try:
        assessment_item = next(assessment_iterator)
        response = assessment_item.to_dict()

        return response
    except StopIteration:
        emit('end', {'assessment': 'end'})
        return ''


@socketio.on('answer')
def handle_answer(answer: str):
    global assessment_item

    result = assessment_item.evaluate(answer)

    return result


@socketio.on('disconnect')
def handle_disconnect():
    global assessment, assessment_iterator, assessment_item

    assessment = None
    assessment_iterator = None
    assessment_item = None
