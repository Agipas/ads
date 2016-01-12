__author__ = 'vwvolodya'

import os
import time
from collections import deque
from pprint import pprint

PROGRAM_NAME = 'wchain'

LABEL = "l"
REAL = "r"
VISITED = "v"
CHILDREN = "c"


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


def compute(path):
    data = from_file(path)
    res = 0
    visited = dict()
    for word in data.itervalues():
        if word[LABEL] in visited:
            continue
        max_depth = 1
        queue = deque([(word, max_depth)])
        while len(queue) > 0:
            cur_node, max_depth = queue.popleft()
            children = [(ch, max_depth + 1) for ch in cur_node[CHILDREN] if ch[LABEL] in data]
            queue.extend(children)
            for child, _ in children:
                visited[child[LABEL]] = None
        if max_depth > res:
            res = max_depth
    return res


def from_file(path):
    with open(path, "r") as input_file:
        # node = {'l': next_string, 'r': False, 'v': False, "c":None}
        words = dict()  # {'label': node}
        real_nodes = dict()
        num_strings = int(input_file.readline())
        for i in xrange(num_strings):
            next_string = input_file.readline().strip()
            node = words.get(next_string, {'l': next_string, "c": None})

            words[node[LABEL]] = node
            real_nodes[node[LABEL]] = node
            children = list()
            # get all sub_strings
            string = node[LABEL]
            labels = set()
            if len(string) > 1:
                labels = {string[:i] + string[i+1:] for i in xrange(len(string))}

            for label in labels:
                n = words.get(label, {'l': label, "c": None})
                words[n[LABEL]] = n
                children.append(n)
            node[CHILDREN] = children
    return real_nodes


def main():
    try:
        res = compute(PROGRAM_NAME + '.in')
        write_result(PROGRAM_NAME + '.out', res)
        pprint("Got production file")
        return
    except (IOError, OSError):
        pass
    path = "../problems/" + PROGRAM_NAME + '/testcases/'
    for _file in os.listdir(path):
        if _file.endswith(".in") or _file.endswith(".txt"):
            pprint('Reading file %s ....' % _file)
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            pprint(res)


if __name__ == '__main__':
    main()
