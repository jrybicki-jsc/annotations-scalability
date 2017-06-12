#!/usr/bin/env python
import sys

# import glob

HEADER = 'set terminal png\n' \
         'set output "output.png"\n' \
         'set xlabel "Runs"\n' \
         'set ylabel "Time [ms]"\n\n'


def decorate_single_file(fname):
    return "'%s' u 1 w li, '%s' u 1:2 w errorbars notitle" % (fname, fname)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage %s file1 file2 [...]' % sys.argv[0])
        exit(1)

    print(HEADER)
    output = ('plot %s' % decorate_single_file(sys.argv[1]))
    for fname in sys.argv[2:]:
        output+=", \\\n%s" % decorate_single_file(fname)

    print output