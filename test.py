#!/usr/bin/env python
import argparse
import csv
import datetime
from progressbar import ProgressBar
from prettytable import PrettyTable
from random import randrange
import time

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


def test_creation(store_function, reps=10):
    for _ in range(reps):
        annotation = generate_annotation(body_id_generator=generate_body_id,
                                         target_id_generator=generate_target_id,
                                         time_generator=get_time)
        store_function(annotation=annotation)


def test_retrieval(retrieve_function, range_limit, reps=10):
    for _ in range(reps):
        random_id = randrange(1, range_limit)
        _ = retrieve_function(random_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Performance tester')
    parser.add_argument('module', choices=['neo', 'mongo', 'dummy'])
    parser.add_argument('runs', type=int, default=5)
    parser.add_argument('reps', type=int, default=10)

    args = parser.parse_args()

    bar = ProgressBar()
    table = PrettyTable(['run', 'write', 'read_target', 'read_body'])

    runs = args.runs
    reps = args.reps
    wtt = args.module
    testing_module = __import__("%s" % wtt)
    b = []

    print 'Testing %s with (%d, %d)' % (wtt, runs, reps)
    for i in bar(range(runs)):
        a = ['Run %s' % i]
        with testing_module.executor() as f:
            start = time.time()
            test_creation(f[0], reps)
            value = time.time() - start
            a.append("{0:.7f}".format(value))

        with testing_module.executor() as f:
            start = time.time()
            test_retrieval(f[1], TARGET_NR, reps)
            value = time.time() - start
            a.append("{0:.7f}".format(value))

        with testing_module.executor() as f:
            start = time.time()
            test_retrieval(f[2], BODY_NR, reps)
            value = time.time() - start
            a.append("{0:.7f}".format(value))

            table.add_row(a)
            b.append(a)

    print(table)
    with open('%s-result.csv' % wtt, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(b)

