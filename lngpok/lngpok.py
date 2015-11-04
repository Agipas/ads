from bisect import insort


def searcher(sorted_array):
    jokers = sum((1 for el in sorted_array if el == 0))
    sorted_array = sorted_array[jokers:]
    results = list()
    max_i = len(sorted_array) - 1
    j = 0
    jokers_left = jokers
    while j < max_i:
        i = j
        count = 1
        jokers_i = jokers
        jokers_left = jokers
        while i <= max_i - 1:
            if sorted_array[i] + 1 != sorted_array[i + 1]:
                if not jokers_i:
                    break
                if sorted_array[i] == sorted_array[i + 1]:
                    jokers_left -= 1
                jokers_i -= 1
            i += 1
            count += 1
        else:
            j += 1
        j = i + 1
        results.append(count)
    count = 0
    if results:
        count = max(results)
    return count + jokers_left


def read_value(path):
    with open(path) as f:
        data = f.readline()
    ar = []
    for el in data.split():
        insort(ar, int(el))
    print ar
    return ar


def write_value(path, result):
    with open(path, 'w') as f:
        f.write(str(result))


def enhanced_searcher(array):
    jokers = sum((1 for el in array if el == 0))
    array = array[jokers:]
    results = [jokers]

    j = 0
    jokers_left = jokers
    max_len = len(array) - 1
    while j < max_len:
        i = 0
        count = 0
        while i < max_len - 1:
            diff = array[i + 1] - array[i]

            i += 1

        j += 1 #TODO change
        results.append(count)

    return max(results)


if __name__ == '__main__':
    arr = read_value('lngpok.in')
    res = searcher(arr)
    write_value('lngpok.out', res)