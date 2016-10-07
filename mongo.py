from pymongo import MongoClient


def setup_mongo():
    client = MongoClient()
    db = client['db']
    annotations = db['collection']
    return annotations


def teardown_mongo(collection):
    collection.database.client.close()


def store_annotation(annotation, annotations):
    return annotations.insert_one(annotation).inserted_id


def retrieve_annotation_by_target(target_id, annotations):
    return retrieve_annotation_by_key_value(annotations=annotations,
                                            key='target.jsonld_id',
                                            value=target_id)


def retrieve_annotation_by_body(body_id, annotations):
    return retrieve_annotation_by_key_value(annotations=annotations,
                                            key='body.jsonld_id',
                                            value=body_id)


def retrieve_annotation_by_key_value(annotations, key, value):
    return annotations.find_one({key: value})
