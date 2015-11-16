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
    max_side = n * min(h, w)
    side = max(max_side, h, w, math.ceil(least_square))
    while True:
        x = int(side / h)  # number of rows
        y = int(side / w)  # number of columns
        if x * y >= n:
            break
        side += 1
    # try to make side smaller
    check = side - 1
    x = int(check / h)  # number of rows
    y = int(check / w)  # number of columns
    if x * y >= n:
        side = max(h, w, math.ceil(least_square))
        while True:
            x = long(side / h)  # number of rows
            y = long(side / w)  # number of columns
            if x * y >= n:
                break
            side += 1
    return long(side)


def solver_2(n, h, w):
    min_side = math.ceil((n * h * w) ** 0.5)
    max_side = n * max(h, w)
    left = min_side
    right = max_side
    side = min_side
    while left < right:
        center = (left + right) / 2
        x = int(center / h)  # number of rows
        y = int(center / w)  # number of columns
        if x * y >= n:
            side = center
            right = center
        else:
            left = center
    return side


def solver_3(n, h, w):
    m1, m2, m3 = sorted((n, h, w))



def main():
    try:
        n, h, w = read_values(PROGRAM_NAME + '.in')
        res = solver_2(n, h, w)
        write_result(PROGRAM_NAME + '.out', '{0}'.format(int(res)))
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    for _file in os.listdir("."):
        if _file.endswith(".txt"):
            print 'Reading file %s ....' % _file
            n, h, w = read_values(_file)
            res = solver(n, h, w)
            print 'Result: ', res


if __name__ == '__main__':
    main()
