import datetime
import timeit
from functools import partial
from random import randrange

import sys

from mongo import setup_mongo, store_annotation as mongo_store, \
    retrieve_annotation_by_target as mongo_by_target, \
    retrieve_annotation_by_body as mongo_by_body

from neo import connect, store_annotation as neo_store, \
    retrieve_annotation_by_target as neo_by_target, \
    retrieve_annotation_by_body as neo_by_body

NR = 1


def get_time():
    return datetime.datetime.utcnow().strftime('%x')


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


## testing part

def test_creation(store_function):
    for _ in range(0, 10, 1):
        annotation = generate_annotation(id_generator=generate_id,
                                         time_generator=get_time)
        store_function(annotation=annotation)


def test_retrieval(retrieve_function):
    for _ in range(0, 10, 1):
        random_id = randrange(1, NR)
        _ = retrieve_function(random_id)

def setup_mongo_tests():
    annotations = setup_mongo()
    store_function = partial(mongo_store, annotations=annotations)
    retrieve_function_1 = partial(mongo_by_target, annotations=annotations)
    retrieve_function_2 = partial(mongo_by_body, annotations=annotations)
    return store_function, retrieve_function_1, retrieve_function_2


def setup_neo_tests():
    graph = connect()
    store_function = partial(neo_store, graph=graph)
    retrieve_function_1 = partial(neo_by_target, graph=graph)
    retrieve_function_2 = partial(neo_by_body, graph=graph)
    return store_function, retrieve_function_1, retrieve_function_2


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'Provide an argument what to test (neo or mongo)?'
        sys.exit(-1)

    wtt = sys.argv[1]
    print 'Testing %s' %wtt


    st = """\
    f1, f2, f3 = setup_tests()
    test_creation(f1)
    """
    print 'Staring test: write'
    value = timeit.timeit(st,
                          setup="from __main__ import setup_%s_tests as "
                                "setup_tests, test_creation" % wtt,
                          number=100)
    print 'Done. Elapsed time %s' % value

    st = """\
        f1, f2, f3 = setup_tests()
        test_retrieval(f2)
        """
    print 'Staring test: read target'
    value = timeit.timeit(st,
                          setup="from __main__ import setup_%s_tests as "
                                "setup_tests, test_retrieval" % wtt,
                          number=100)
    print 'Done. Elapsed time %s' % value

    st = """\
            f1, f2, f3 = setup_tests()
            test_retrieval(f3)
            """
    print 'Staring test: read body'
    value = timeit.timeit(st,
                          setup="from __main__ import setup_%s_tests as "
                                "setup_tests, test_retrieval" % wtt,
                          number=100)
    print 'Done. Elapsed time %s' % value
