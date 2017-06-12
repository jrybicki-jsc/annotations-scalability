#!/usr/bin/env python

import sys
import numpy as np


def get_data_from_file(fname):
    print 'Analyzing %s' %fname
    writes = np.genfromtxt(fname, usecols=(1), delimiter=',')
    reads1 = np.genfromtxt(fname, usecols=(2), delimiter=',')
    reads2 = np.genfromtxt(fname, usecols=(3), delimiter=',')

    return writes, reads1, reads2


def merge_data_from_files(file_list):
    w, r1, r2 = get_data_from_file(file_list[0])

    for fname in file_list[1:]:
        a, b, c = get_data_from_file(fname)
        w = np.vstack((w, a))
        r1 = np.vstack((r1, b))
        r2 = np.vstack((r2, c))

    return w, r1, r2


def store_to_file(vector, fname):
    with open(fname, 'w') as f:
        print 'Storing in %s (%d records)' % (fname, len(vector.mean(0)))
        for i in range(0, len(vector.mean(0))):
            f.write('%f\t%f\n' % (vector.mean(0)[i], vector.std(0)[i]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage %s file1 file2 [...]' % sys.argv[0]
        exit(1)

    w, r1, r2 = merge_data_from_files(sys.argv[1:])

    store_to_file(w, 'writes.res')
    store_to_file(r1, 'targets.res')
    store_to_file(r2, 'bodies.res')
