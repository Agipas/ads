__author__ = 'vwvolodya'
import os
import math


PROGRAM_NAME = 'bugtrk'


def read_values(path):
    with open(path) as f:
        data = f.readline().split()
        N, h, w = [int(i) for i in data]
        return N, h, w


def write_result(path, result):
    with open(path, 'w') as f:
        f.write(str(result))


def solver(n, h, w):
    least_square = (n * h * w) ** 0.5
    side = max(h, w, math.ceil(least_square))
    while True:
        x = int(side / h)    # number of rows
        y = int(side / w)    # number of columns
        if x * y >= n:
            break
        side += 1
    return side


def main():
    try:
        n, h, w = read_values(PROGRAM_NAME + '.in')
        res = solver(n, h, w)
        write_result(PROGRAM_NAME + '.out', '{0}'.format(res))
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    for _file in os.listdir("."):
        if _file.endswith(".txt"):
            print 'Reading file %s ....' %_file
            n, h, w = read_values(_file)
            res = solver(n, h, w)
            print 'Result: ', res


if __name__ == '__main__':
    main()
