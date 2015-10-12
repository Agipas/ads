__author__ = 'vholubets'


def read_file(path):
    with open(path) as f:
        prices = f.readline()
        discount = f.readline()
        prices = [int(num) for num in prices.split()]
        discount = float(discount.strip())
        return prices, discount


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def swap(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp


def sorting(array):
    for i in range(0, len(array)):
        min_index = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min_index]:
                min_index = j
        swap(array, i, min_index)


def main():
    allowed_disc_num = 3
    input_file = 'dscnt.in'
    output_file = 'dscnt.out'
    prices, disc = read_file(input_file)
    sorting(prices)
    actual_disc_num = len(prices) / allowed_disc_num
    res = sum(prices[:-actual_disc_num]) + sum(
        [i * (100 - disc)/100. for i in prices[-actual_disc_num:]])
    write_file(output_file, "{0:.2f}".format(res))


if __name__ == '__main__':
    main()
