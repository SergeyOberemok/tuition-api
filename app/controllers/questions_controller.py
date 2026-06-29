from flask import Blueprint, request
from bson import ObjectId
from bson.json_util import dumps
from db import get_db
from utils import deserialize_model
from utils.deserialize_model import deserialize_doc, assign_missing_ids_on_items
from utils.serialize_model import serialize_docs, serialize_doc

questions_blueprint = Blueprint('questions', __name__)


@questions_blueprint.route('/')
def find_all():
    # id_value = request.args.get('id')
    questions = get_db().questions.find({})

    return dumps(serialize_docs(questions))


@questions_blueprint.route('/<question_id>')
def question(question_id: str):
    question = get_db().questions.find_one_or_404({'_id': ObjectId(question_id)})

    return serialize_doc(question)


@questions_blueprint.route('/', methods=['POST'])
def create():
    data = assign_missing_ids_on_items(request.get_json())

    result = get_db().questions.insert_one(data)
    question = get_db().questions.find_one({'_id': result.inserted_id})

    return serialize_doc(question)


@questions_blueprint.route('/<question_id>', methods=['PUT'])
def update(question_id: str):
    data = deserialize_doc(request.get_json())

    result = get_db().questions.update_one({'_id': ObjectId(question_id)}, {'$set': data})

    return 'True' if result.modified_count > 0 else 'False'


@questions_blueprint.route('/<question_id>', methods=['DELETE'])
def delete(question_id: str):
    result = get_db().questions.delete_one({'_id': ObjectId(question_id)})

    return 'True' if result.deleted_count > 0 else 'False'
