from bisect import insort


def read_value(path):
    with open(path) as f:
        data = f.readline()
    ar = []
    for el in data.split():
        insort(ar, int(el))
    return ar


def write_value(path, result):
    with open(path, 'w') as f:
        f.write(str(result))


def searcher(sorted_array):
    jokers = sum((1 for el in sorted_array if el == 0))
    sorted_array = sorted_array[jokers:]
    results = list()
    max_i = len(sorted_array) - 1
    j = 0
    while j < max_i:
        i = j
        count = 1
        jokers_i = jokers
        while i <= max_i - 1:
            if sorted_array[i] + 1 != sorted_array[i + 1]:
                if not jokers_i:
                    break
                jokers_i -= 1
            i += 1
            count += 1
        else:
            j += 1
        j = i + 1
        results.append(count)
    return max(results) + jokers


if __name__ == '__main__':
    arr = read_value('lngpok.in')
    res = searcher(arr)
    write_value('lngpok.out', res)