__author__ = 'vwvolodya'

import heapq
import string
import random
import time
from pprint import pprint
import os

PROGRAM_NAME = 'wchain'


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r  %2.3f seconds' % (method.__name__.upper(), te - ts)
        return result
    return timed


def read_file(path):
    result = list()
    with open(path) as f:
        lines = int(f.readline())
        while lines > 0:
            result.append(f.readline().strip())
            lines -= 1
    return result


def write_result(path, result):
    with open(path, 'w') as f:
        if isinstance(result, list):
            for el in result:
                f.write(str(el) + '\n')
        else:
            f.write(str(result))


def compute(path):
    data = read_file(path)
    return data


def main():
    try:
        res = compute(PROGRAM_NAME + '.in')
        write_result(PROGRAM_NAME + '.out', res)
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    path = "../problems/" + PROGRAM_NAME + '/testcases/'
    for _file in os.listdir(path):
        if _file.endswith(".txt") or _file.endswith(".in"):
            print 'Reading file %s ....' % _file
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            pprint(res)


if __name__ == '__main__':
    main()

