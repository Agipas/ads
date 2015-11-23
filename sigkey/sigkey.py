__author__ = 'vwvolodya'
import time
import os
import string
from main import IndexedString

PROGRAM_NAME = os.path.splitext(os.path.basename(__file__))[0]


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r  %2.3f seconds' % (method.__name__.upper(), te - ts)
        return result
    return timed


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


def compute(path):
    keys = read_values(path)
    return solver(keys)


def main():
    try:
        res = compute(PROGRAM_NAME + '.in')
        write_result(PROGRAM_NAME + '.out', '{0}'.format(res))
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    for _file in os.listdir("."):
        if _file.endswith(".txt") or _file.endswith(".in"):
            print 'Reading file %s ....' % _file
            res = compute(_file)
            print 'Result: ', res


@timeit
def solver(keys):
    letters = string.ascii_lowercase
    checking_dict = dict((k, v) for k, v in zip(letters, range(1, len(letters) + 1)))
    keys = [k for k in keys if len(set(k)) == len(k)]
    keys = [''.join(sorted(key)) for key in keys]
    start = list()
    end = list()
    for el in keys:
        if el[0] == 'a':
            start.append(el)
        else:
            end.append(el)
    indexed = IndexedString()
    for el in end:
        indexed.add_key(el)

    count = 0
    for el in start:
        length = checking_dict[el[-1]]
        subtraction_set = set(letters[:length])
        looking_for = ''.join(sorted(subtraction_set - set(el))) or letters[len(el)]
        result = indexed.search_key(looking_for)
        el_set = set(el)
        if result == -1:
            continue
        for item in result:
            if el_set - set(item) == el_set:
                count += 1
                break
    return count


if __name__ == '__main__':
    main()
