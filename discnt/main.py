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
    arr[i] = arr[i] ^ arr[j]
    arr[j] = arr[i] ^ arr[j]
    arr[i] = arr[i] ^ arr[j]


def compare(a, b):
    return a > b


def _merge(arr1, arr2):
    result = array('i')
    i = 0
    j = 0
    while i < len(arr1):
        pass


def merge_sort_bottom_up():
    tmp = array('i', [])

