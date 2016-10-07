import datetime
import timeit
from functools import partial
from random import randrange
import sys
from progressbar import ProgressBar
from prettytable import PrettyTable

from mongo import setup_mongo, store_annotation as mongo_store, \
    retrieve_annotation_by_target as mongo_by_target, \
    retrieve_annotation_by_body as mongo_by_body, teardown_mongo

from neo import connect, store_annotation as neo_store, \
    retrieve_annotation_by_target as neo_by_target, \
    retrieve_annotation_by_body as neo_by_body, create_constraints, disconnect

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


class mongo_executor:
    def __enter__(self):
        self.annotations = setup_mongo()
        store_function = partial(mongo_store, annotations=self.annotations)
        retrieve_function_1 = partial(mongo_by_target,
                                      annotations=self.annotations)
        retrieve_function_2 = partial(mongo_by_body,
                                      annotations=self.annotations)
        return store_function, retrieve_function_1, retrieve_function_2

    def __exit__(self, exc_type, exc_val, exc_tb):
        teardown_mongo(self.annotations)


class neo_executor:
    def __enter__(self):
        self.graph = connect()
        create_constraints(self.graph)
        store_function = partial(neo_store, graph=self.graph)
        retrieve_function_1 = partial(neo_by_target, graph=self.graph)
        retrieve_function_2 = partial(neo_by_body, graph=self.graph)
        return store_function, retrieve_function_1, retrieve_function_2

    def __exit__(self, exc_type, exc_val, exc_tb):
        disconnect(self.graph)


class empty_executor:
    def __enter__(self):
        def empty_function(annotation):
            pass
        return (empty_function,) * 3

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass



def log(param):
    # print param
    pass


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] not in ['neo', 'mongo', 'empty']:
        print 'Provide an argument what to test (neo or mongo)?'
        sys.exit(-1)

    bar = ProgressBar()
    table = PrettyTable(['run', 'write', 'read_target', 'read_body'])

    runs = 5
    reps = 10

    wtt = sys.argv[1]
    for i in bar(range(1, runs)):
        a = ['Run %s' % i]
        log('Starting %s write tests' % wtt)
        st = """\
with executor() as f:
    test_creation(f[0])
        """
        value = timeit.timeit(st,
                              setup="from __main__ import %s_executor as "
                                    "executor, test_creation" % wtt,
                              number=reps)
        log('%s write result: %s' % (wtt, value))
        a.append("{0:.7f}".format(value))

        log('Starting %s read_target tests' % wtt)
        st = """\
with executor() as f:
    test_retrieval(f[1], TARGET_NR)
            """
        value = timeit.timeit(st,
                              setup="from __main__ import %s_executor as "
                                    "executor, TARGET_NR, test_retrieval" %
                                    wtt,
                              number=reps)
        log('%s read_target result: %s' % (wtt, value))
        a.append("{0:.7f}".format(value))

        st = """\
with executor() as f:
    test_retrieval(f[2], BODY_NR)
        """
        log('Staring %s read_body tests' % wtt)
        value = timeit.timeit(st,
                              setup="from __main__ import %s_executor as "
                                    "executor, BODY_NR, test_retrieval" % wtt,
                              number=reps)
        log('%s read_target result %s' % (wtt, value))
        a.append("{0:.7f}".format(value))
        table.add_row(a)

    print table
