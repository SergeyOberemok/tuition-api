from flask import Blueprint

index_blueprint = Blueprint('/', __name__)

@index_blueprint.route('/ping')
def pong_hello_world():
    return 'pong hello world'