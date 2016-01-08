import os
import time
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
    max_exp = 0
    data = data[::-1]
    for i in xrange(1, levels + 1):
        for j in xrange(levels + 1 - i):
            s_1 = solutions[i - 1][j]
            d_1 = data[i - 1][j]
            case1 = s_1 + d_1
            s_2 = solutions[i - 1][j + 1]
            d_2 = d_1
            case2 = s_2 + d_2
            solutions[i][j] = max(case1, case2)
        max_exp = solutions[levels][0]
    return max_exp


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

