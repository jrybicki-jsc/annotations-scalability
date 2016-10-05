from pymongo import MongoClient
import datetime
import timeit
from functools import partial
from random import randrange

NR = 1


def get_time():
    return datetime.datetime.utcnow()


def generate_id():
    global NR
    NR += 1
    return "http://domain.com/%s" % (NR)


def generate_annotation(time_generator, id_generator):
    annotation = dict(
        body={
            "jsonld_id": id_generator()
        },
        target={
            "jsonld_id": id_generator()
        },
        created=time_generator()
    )
    return annotation


# mongo part

def setup_mongo():
    client = MongoClient()
    db = client['db']
    annotations = db['collection']
    return annotations


def store_annotation(annotation, annotations):
    anno_id = annotations.insert_one(annotation).inserted_id
    return anno_id


def retrieve_annotation_by_target(target_id, annotations):
    return retrieve_annotation_by_key_value(annotations=annotations,
                                            key='target.jsonld_id',
                                            value=target_id)


def retrieve_annotation_by_body(body_id, annotations):
    return retrieve_annotation_by_key_value(annotations=annotations,
                                            key='body.jsonld_id',
                                            value=body_id)


def retrieve_annotation_by_key_value(annotations, key, value):
    anno2 = annotations.find_one({key: value})
    return anno2


## testing part

def test_creation(store_function):
    for _ in range(0, 10, 1):
        annotation = generate_annotation(id_generator=generate_id,
                                         time_generator=get_time)
        store_function(annotation=annotation)


def test_retrieval(retrive_function):
    for _ in range(0, 10, 1):
        random_id = randrange(1, NR)
        ret = retrive_function(random_id)


def do_mongo_test_1():
    annotations = setup_mongo()
    annotation_store = partial(store_annotation, annotations=annotations)
    test_creation(annotation_store)


def do_mongo_test_2():
    annotations = setup_mongo()
    retrive_function = partial(retrieve_annotation_by_target,
                               annotations=annotations)
    test_retrieval(retrive_function)


def do_mongo_test_3():
    annotations = setup_mongo()
    retrive_function = partial(retrieve_annotation_by_body,
                               annotations=annotations)
    test_retrieval(retrive_function)


if __name__ == "__main__":
    print 'Staring test: write'
    value = timeit.timeit("do_mongo_test_1()", setup="from __main__ import "
                                                     "do_mongo_test_1",
                          number=100)
    print 'Done. Elapsed time %s' % value

    print 'Staring test: read target'
    value = timeit.timeit("do_mongo_test_2()", setup="from __main__ import "
                                                     "do_mongo_test_2",
                          number=100)
    print 'Done. Elapsed time %s' % value

    print 'Staring test: read body'
    value = timeit.timeit("do_mongo_test_3()", setup="from __main__ import "
                                                     "do_mongo_test_3",
                          number=100)
    print 'Done. Elapsed time %s' % value
