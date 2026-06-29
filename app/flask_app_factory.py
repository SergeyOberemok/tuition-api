from flask import Flask
from .controllers.index_controller import index_blueprint
from .controllers.questions_controller import questions_blueprint


def create_flask_app():
    app = Flask(__name__, template_folder='dist', static_folder='dist', static_url_path='/')

    app.register_blueprint(index_blueprint, url_prefix='/api')
    app.register_blueprint(questions_blueprint, url_prefix='/api/questions')

    return app
