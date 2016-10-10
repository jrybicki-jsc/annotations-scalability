import os
from functools import partial
from pymongo import MongoClient


def setup_mongo():
    host = os.getenv("MONGO_PORT_27017_TCP_ADDR", "localhost")
    port = os.getenv("MONGO_PORT_27017_TCP_PORT", "27017")
    client = MongoClient("mongodb://%s:%s" % (host, port))
    db = client['db']
    annotations = db['collection']
    return annotations

class executor:
    def __enter__(self):
        self.annotations = setup_mongo()
        store_function = partial(store_annotation, annotations=self.annotations)
        retrieve_function_1 = partial(retrieve_annotation_by_target,
                                      annotations=self.annotations)
        retrieve_function_2 = partial(retrieve_annotation_by_body,
                                      annotations=self.annotations)
        return store_function, retrieve_function_1, retrieve_function_2

    def __exit__(self, exc_type, exc_val, exc_tb):
        teardown_mongo(self.annotations)

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
