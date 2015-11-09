# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:34:32 2015

@author: vwvolodya
"""


class Homyak(object):
    def __init__(self, h, g):
        self.h = h
        self.g = g

    def __str__(self):
        return 'g: {0}, h: {1}'.format(self.g, self.h)

    def __repr__(self):
        return str(self) + ' ##Sum: {0}##'.format(self.h + 1 * self.g)

    def sum(self, n):
        return (n - 1) * self.g + self.h


class HomeForHomyaks(list):
    def get_sum(self):
        l = len(self)
        return sum(((l - 1) * el.g + el.h) for el in self)

    def custom_sort(self, n):
        l = n - 1
        self.sort(key=lambda el: l * el.g + el.h)


def read_values(path):
    with open(path) as f:
        budget = int(f.readline())
        num_homyak = int(f.readline())
        line = 0
        array = HomeForHomyaks()
        while line < num_homyak:
            h, g = f.readline().split()
            h, g = int(h), int(g)
            array.append(Homyak(h, g))
            line += 1
        print budget
        return budget, array


def write_result(path, result):
    with open(path, 'w') as f:
        f.write(result)


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


def maxim(budget, array):
    result = list()
    print len(array)

    for i in xrange(1, len(array) + 1):
        count = 0
        remainder = budget
        array.custom_sort(i)
        for j, el in enumerate(array):
            current_cost = el.sum(i)
            if current_cost > remainder or j > i - 1:
                print 'yeh'
                break
            count += 1
            remainder -= current_cost
        if result:
            if count > result[-1]:
                result.append(count)
            else:
                print result
                break
        else:
            result.append(count)
    return max(result)


def maxim_log(budget, array):
    result = list()
    print len(array)

    left = 0
    right = len(array)
    while left < right:
        i = (left + right) / 2
        count = 0
        remainder = budget
        array.custom_sort(i)
        for j, el in enumerate(array):
            current_cost = el.sum(i)
            if current_cost > remainder or j > i:
                print 'yeh'
                break
            count += 1
            remainder -= current_cost
        if result:
            if count > result[-1]:
                result.append(count)
                left = i
            else:
                right = i
        else:
            result.append(count)
    return max(result)


if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()
    bud, arr = read_values('hamstr.in')
    # bud, arr = read_values('data.txt')
    # res = maximizer(bud, merge_sort(arr))
    res = maxim_log(bud, arr)
    write_result('hamstr.out', '{0}'.format(res))
    print res
    print (datetime.now() - start).total_seconds()
