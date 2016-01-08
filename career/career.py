import time
import os
from pprint import pprint


PROGRAM_NAME = 'career'


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r  %2.3f seconds' % (method.__name__.upper(), te - ts)
        return result

    return timed


def write_result(path, result):
    with open(path, 'w') as f:
        if isinstance(result, list):
            for el in result:
                f.write(str(el) + '\n')
        else:
            f.write(str(result))


def read_values(path):
    result = list()
    solutions = list()
    with open(path) as f:
        levels = int(f.readline())
        for _ in xrange(levels):
            data = f.readline().strip().split()
            result.append([int(i)for i in data])
    for i in xrange(levels+1):
        solutions.append([0 for _ in xrange(levels + 1)])
    return result, solutions, levels


def compute(path):
    data, solutions, levels = read_values(path)
    for j in xrange(1, levels + 1):
        for i in xrange(levels):
            s1 = solutions[j][i - 1]
            d1 = data[i - 1][j]
            case_1 = s1 + d1
            s2 = solutions[j + 1][i - 1]
            d2 = data[i - 1][j]
            case_2 = s2 + d2
            solutions[j][i] = max(case_1, case_2)
    return solutions[levels][0]


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
        if _file.endswith(".in"): # or _file.endswith(".in"):
            print 'Reading file %s ....' % _file
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            pprint(res)


if __name__ == '__main__':
    main()

