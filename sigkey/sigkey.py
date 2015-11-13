__author__ = 'vwvolodya'
import os
import string


PROGRAM_NAME = 'bugtrk'


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
    length = len(keys)
    # res = 0
    # for i in xrange(0, length):
    #     for j in xrange(i+1, length):
    #         tmp = sorted(keys[i]+keys[j])
    #         if checking_dict[len(tmp)] == tmp[-1]:
    #             res += 1
    res = sum((1 for i in xrange(length) for j in xrange(i+1, length)
               if checking_dict[len(sorted(keys[i]+keys[j]))] == sorted(keys[i]+keys[j])[-1]))
    return res


def main():
    try:
        keys = read_values(PROGRAM_NAME + '.in')
        res = solver(keys)
        write_result(PROGRAM_NAME + '.out', '{0}'.format(res))
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    for _file in os.listdir("."):
        if _file.endswith(".txt"):
            print 'Reading file %s ....' %_file
            keys = read_values(_file)
            res = solver(keys)
            print 'Result: ', res


if __name__ == '__main__':
    main()
