# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:34:32 2015

@author: vwvolodya
"""


class Homyak(object):
    def __init__(self, h, g):
        self.h = h
        self.g = g

    def __cmp__(self, other):
        assert isinstance(other, Homyak)
        current_sum = self.g + self.h
        other_sum = other.g + other.h
        if current_sum < other_sum:
            return -1
        elif current_sum == other_sum:
            return 0
        else:
            return 1

    def __str__(self):
        return 'Homyak -- g: {0}, h: {1}'.format(self.g, self.h)

    def __repr__(self):
        return str(self) + ' Sum: {0}'.format(self.h + self.g)

    @property
    def sum(self):
        return self.g + self.h


def read_values(path):
    with open(path) as f:
        budget = int(f.readline())
        num_homyak = int(f.readline())
        line = 0
        array = []
        while line < num_homyak:
            h, g = f.readline().split()
            h, g = int(h), int(g)
            array.append(Homyak(h, g))
            line += 1
        print budget, sorted(array)
        return budget, array


def write_result(path, result):
    with open(path, 'w') as f:
        f.write(result)


def _randoms():
    ar = []
    import random as r
    i = 10
    while i > 0:
        ar.append(Homyak(r.randint(1, 100), r.randint(2, 100)))
        i -= 1
    print ar
    print sorted(ar)


def maximizer(budget, sorted_array):
    count = 0
    remainder = budget
    for el in sorted_array:
        if el.sum > remainder:
            break
        count += 1
        remainder -= el.sum
    if count == 0:
        # count = [1 for el in sorted_array if budget >= el.h].pop()
        for el in sorted_array:
            if budget >= el.h:
                count = 1
            else:
                break
    return count


def merge_sort(lst):
    if not lst:
        return []
    lists = [[x] for x in lst]
    while len(lists) > 1:
        lists = merge_lists(lists)
    return lists[0]


def merge_lists(lists):
    result = []
    for i in range(0, len(lists) // 2):
        result.append(merge2(lists[i * 2], lists[i * 2 + 1]))
    if len(lists) % 2:
        result.append(lists[-1])
    return result


def merge2(xs, ys):
    i = 0
    j = 0
    result = []
    while i < len(xs) and j < len(ys):
        x = xs[i]
        y = ys[j]
        if x > y:
            result.append(y)
            j += 1
        else:
            result.append(x)
            i += 1
    result.extend(xs[i:])
    result.extend(ys[j:])
    return result


if __name__ == '__main__':
    bud, arr = read_values('hamstr.in')
    res = maximizer(bud, merge_sort(arr))
    write_result('hamstr.out', '{0}'.format(res))
