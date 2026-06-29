import hashlib
import uuid


def generate_question_id() -> str:
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()