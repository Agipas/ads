import sys


def main():
    input_filename = "discnt.in" if len(sys.argv) == 1 else sys.argv[1]
    output_filename = "discnt.out" if len(sys.argv) == 1 else sys.argv[2]

    prices, discount_rate = read_input(input_filename)
    min_purchase_sum = solve(prices, discount_rate)
    write_output(output_filename, min_purchase_sum)


def read_input(filename):
    with open(filename, "r") as input_file:
        prices = [int(price_str) for price_str in input_file.readline().split()]
        discount_rate = int(input_file.readline())
        return prices, discount_rate


def solve(prices, discount_rate):
    insertion_sort(prices)
    num_discounted_items = len(prices) / 3
    for i in range(0, num_discounted_items):
        prices[i] *= ((100.0 - discount_rate) / 100)
    return sum(prices)


def insertion_sort(array):
    for i in xrange(1, len(array)):
        j = i
        # Sort in descending order
        while j > 0 and array[j - 1] < array[j]:
            array[j - 1], array[j] = array[j], array[j - 1]
            j -= 1


def write_output(filename, min_purchase_sum):
    with open(filename, "w") as output_file:
        output_file.write("%.2f" % min_purchase_sum)


if __name__ == "__main__":
    main()
