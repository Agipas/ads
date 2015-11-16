__author__ = 'vwvolodya'
import os
import string
import random


PROGRAM_NAME = os.path.splitext(os.path.basename(__file__))[0]


def read_values(path):
    with open(path) as f:
        count = int(f.readline())
        keys = list()
        while count > 0:
            keys.append(f.readline().strip())
            count -= 1
        return keys


def write_result(path, result):
    with open(path, 'w') as f:
        f.write(str(result))


def solver(keys):
    checking_dict = dict(((k, v) for k, v in zip(range(1, 27), string.ascii_lowercase)))
    res = 0
    random.shuffle(keys)
    for i, el in enumerate(keys):
        for j in xrange(i, len(keys)):
            if i == j:
                continue
            second = keys[j]
            tmp = sorted(el + second)
            if checking_dict.get(len(tmp)) == tmp[-1]:
                res += 1
                keys.remove(el)
                keys.remove(second)
                break
        else:
            continue
    return res


def solver_2(keys):
    checking_dict = dict(((k, v) for k, v in zip(range(1, 27), string.ascii_lowercase)))
    potential_start_of_key = [k for k in keys if 'a' in k]
    potential_end_of_key = [k for k in keys if 'a' not in k]
    count = 0
    for el in potential_start_of_key:
        for ell in potential_end_of_key:
            tmp = sorted(el + ell)
            if checking_dict.get(len(tmp)) == tmp[-1]:
                count += 1
                potential_end_of_key.remove(ell)
                break
    return count


def solver_3(keys):
    pass


def main():
    try:
        keys = read_values(PROGRAM_NAME + '.in')
        res = solver_2(keys)
        write_result(PROGRAM_NAME + '.out', '{0}'.format(res))
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    for _file in os.listdir("."):
        if _file.endswith(".txt") or _file.endswith(".in"):
            print 'Reading file %s ....' % _file
            keys = read_values(_file)
            res = solver(keys)
            print 'Result: ', res


if __name__ == '__main__':
    main()