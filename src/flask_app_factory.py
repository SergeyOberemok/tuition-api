from flask import Flask

from src.controllers.assessment_controller import socketio
from src.controllers.index_controller import index_blueprint
from src.controllers.questions_controller import questions_blueprint


def create_flask_app():
    app = Flask(__name__, template_folder='dist', static_folder='dist', static_url_path='/')

    app.register_blueprint(index_blueprint, url_prefix='/api')
    app.register_blueprint(questions_blueprint, url_prefix='/api/questions')
    socketio.init_app(app)

    return app, socketio
