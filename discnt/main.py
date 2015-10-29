__author__ = 'vholubets'

from array import array


def read_file(path):
    with open(path) as f:
        prices = f.readline()
        discount = f.readline()
        prices = [int(num) for num in prices.split()]
        discount = float(discount.strip())
        prices = array('i', prices)
        return prices, discount


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def swap(arr, i, j):
    # not pythonic way to swap
    arr[i] = arr[i] ^ arr[j]
    arr[j] = arr[i] ^ arr[j]
    arr[i] = arr[i] ^ arr[j]


def compare(a, b):
    return a > b


def _merge(arr, results, left_begin, right_begin, right_end):
    left_end = right_begin - 1
    left_read_pos = left_begin
    right_read_pos = right_begin
    result_write_pos = left_begin
    while left_read_pos <= left_end and right_read_pos <= right_end:
        if compare(arr[left_read_pos], arr[right_read_pos]):
            results[result_write_pos] = arr[left_read_pos]
            left_read_pos += 1
        else:
            results[result_write_pos] = arr[right_read_pos]
            right_read_pos += 1
        result_write_pos += 1
    while left_read_pos <= left_end:
        results[result_write_pos] = arr[left_read_pos]
        result_write_pos += 1
        left_read_pos += 1
    while right_read_pos <= right_end:
        results[result_write_pos] = arr[left_read_pos]
        left_read_pos += 1
        result_write_pos += 1
    i = left_begin
    while i < right_end:
        arr[i] = results[i]
        i += 1


def sort(arr):
    size = 1
    length = len(arr)
    result = array('i', [0] * length)  # allocate memory
    while size < length:
        i = 0
        while i < length:
            _merge(arr, result, i, i + size, i + 2 * size)
            i += 2 * size
        size *= 2


if __name__ == '__main__':
    import random

    arr = array('i', [random.randint(0, 1000) for _ in range(100)])
    print sort(arr)
