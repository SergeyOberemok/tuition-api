def serialize_doc(doc: dict) -> dict:
    if '_id' not in doc:
        return doc

    doc['id'] = str(doc.pop('_id'))

    for (key, value) in doc.items():
        if type(value) is list and len(value) > 0:
            doc[key] = serialize_docs(value)

    return doc


def serialize_docs(docs: list[dict]) -> list[dict]:
    return [serialize_doc(doc) for doc in docs]
