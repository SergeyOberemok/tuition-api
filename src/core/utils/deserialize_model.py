from bson import ObjectId


def deserialize_doc(doc: dict) -> dict:
    if 'id' not in doc:
        return doc

    doc['_id'] = ObjectId(doc.pop('id'))

    for (key, value) in doc.items():
        if (type(value) is list) and (len(value) > 0):
            doc[key] = deserialize_docs(value)

    return doc


def deserialize_docs(docs: list[dict]) -> list[dict]:
    return [deserialize_doc(doc) for doc in docs]


def assign_missing_ids_on_items(doc: dict) -> dict:
    for item in doc.get('items', []):
        item['_id'] = ObjectId()

    return doc
