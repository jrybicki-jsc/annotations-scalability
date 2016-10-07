import datetime
import timeit
from functools import partial
from random import randrange
import sys
from progressbar import ProgressBar
from prettytable import PrettyTable

from mongo import setup_mongo, store_annotation as mongo_store, \
    retrieve_annotation_by_target as mongo_by_target, \
    retrieve_annotation_by_body as mongo_by_body

from neo import connect, store_annotation as neo_store, \
    retrieve_annotation_by_target as neo_by_target, \
    retrieve_annotation_by_body as neo_by_body, create_constraints

TARGET_NR = 1

BODY_NR = 1


def generate_target_id():
    global TARGET_NR
    TARGET_NR += 1
    return "http://domain.com/%s" % TARGET_NR


def generate_body_id():
    global BODY_NR
    BODY_NR += 1
    return "body_%s" % BODY_NR


def get_time():
    return datetime.datetime.utcnow().strftime('%x')


def generate_annotation(time_generator, body_id_generator,
                        target_id_generator):
    annotation = dict(
        body={
            "jsonld_id": body_id_generator()
        },
        target={
            "jsonld_id": target_id_generator()
        },
        created=time_generator()
    )
    return annotation


## testing part

def test_creation(store_function):
    for _ in range(0, 10, 1):
        annotation = generate_annotation(body_id_generator=generate_body_id,
                                         target_id_generator=generate_target_id,
                                         time_generator=get_time)
        store_function(annotation=annotation)


def test_retrieval(retrieve_function, range_limit):
    for _ in range(0, 10, 1):
        random_id = randrange(1, range_limit)
        _ = retrieve_function(random_id)


def setup_mongo_tests():
    annotations = setup_mongo()
    store_function = partial(mongo_store, annotations=annotations)
    retrieve_function_1 = partial(mongo_by_target, annotations=annotations)
    retrieve_function_2 = partial(mongo_by_body, annotations=annotations)
    return store_function, retrieve_function_1, retrieve_function_2


def setup_neo_tests():
    graph = connect()
    create_constraints(graph)
    store_function = partial(neo_store, graph=graph)
    retrieve_function_1 = partial(neo_by_target, graph=graph)
    retrieve_function_2 = partial(neo_by_body, graph=graph)
    return store_function, retrieve_function_1, retrieve_function_2


def setup_empty_tests():
    def empty_function(annotation):
        pass

    return (empty_function,) * 3


def log(param):
    # print param
    pass

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] not in ['neo', 'mongo', 'empty']:
        print 'Provide an argument what to test (neo or mongo)?'
        sys.exit(-1)

    bar = ProgressBar()
    table = PrettyTable(['run', 'write', 'read_target', 'read_body'])

    wtt = sys.argv[1]
    for i in bar(range(1, 5)):
        a = ['Run %s' % i]
        log('Starting %s write tests' % wtt)
        st = """\
f1, f2, f3 = setup_tests()
test_creation(f1)
        """
        value = timeit.timeit(st,
                              setup="from __main__ import setup_%s_tests as "
                                    "setup_tests, test_creation" % wtt,
                              number=1000)
        log('%s write result: %s' % (wtt, value))
        a.append(value)

        log('Starting %s read_target tests' % wtt)
        st = """\
f1, f2, f3 = setup_tests()
test_retrieval(f2, TARGET_NR)
            """
        value = timeit.timeit(st,
                              setup="from __main__ import setup_%s_tests as "
                                    "setup_tests, TARGET_NR, test_retrieval" % wtt,
                              number=1000)
        log('%s read_target result: %s' % (wtt, value))
        a.append(value)

        st = """\
f1, f2, f3 = setup_tests()
test_retrieval(f3, BODY_NR)
        """
        log('Staring %s read_body tests' % wtt)
        value = timeit.timeit(st,
                              setup="from __main__ import setup_%s_tests as "
                                    "setup_tests, BODY_NR, test_retrieval" % wtt,
                              number=1000)
        log('%s read_target result %s' % (wtt, value))
        a.append(value)
        table.add_row(a)

    print table
