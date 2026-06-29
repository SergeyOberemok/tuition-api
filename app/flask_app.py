from flask import render_template
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os

from .flask_app_factory import create_flask_app
from app.assessment.Assessments import AssessmentFactory
from app.strategies.Strategies import CalculationStrategyFactory
from app.utils.number_utils import generateRandomNumbersPairs
from db import init_db

load_dotenv()

app = create_flask_app()
app.config['MONGO_URI'] = os.getenv('DB_URI')
init_db(app)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

assessment = None
assessment_iterator = None
assessment_item = None


def start_assessment(quantity: int):
    numbers_pairs = generateRandomNumbersPairs(maxNumber=10, count=quantity)
    strategies = CalculationStrategyFactory.createAdditionStrategies(numbers_pairs)

    assessment = AssessmentFactory.createResponseAssessment(strategies)
    assessment_iterator = iter(assessment)

    return assessment, assessment_iterator


@socketio.on('start')
def handle_start(quantity: int):
    global assessment, assessment_iterator

    assessment, assessment_iterator = start_assessment(quantity)


@socketio.on('question')
def handle_question(args):
    global assessment_item

    try:
        assessment_item = next(assessment_iterator)

        return str(assessment_item), assessment_item.goal
    except StopIteration:
        emit('end', {'assessment': str(assessment), 'results': assessment.results, 'isPassed': assessment.result})
        return ''


@socketio.on('answer')
def handle_answer(answer: int):
    result = assessment_item.pipe(lambda item: item.setAnswer(lambda: answer)).assess()

    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image/<int:digit>')
def fetch_image(digit: int):
    return f'{digit}'


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
