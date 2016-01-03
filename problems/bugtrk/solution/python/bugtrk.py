import sys


def main():
    input_filename = "bugtrk.in" if len(sys.argv) == 1 else sys.argv[1]
    output_filename = "bugtrk.out" if len(sys.argv) == 1 else sys.argv[2]

    count, width, height = read_input(input_filename)
    min_size = solve(count, width, height)
    write_output(output_filename, min_size)


def read_input(filename):
    with open(filename, "r") as input_file:
        count, width, height = [int(param) for param in input_file.readline().split()]
        return count, width, height


def solve(count, width, height):
    # Checking if it's possible to fit everything on a board of size exactly 'candidate_size'.
    # Since 'candidate_size' is a sorted sequence from 1 to [some large number],
    # we can use binary search instead of linear search to locate the optimal size faster.
    left = 1
    right = count * max(width, height)

    # Since we're interested in the minimum size (not just arbitrary suitable size),
    # we need to find the leftmost item among the suitable ones.
    # Comparisons and boundary arithmetics are very important here.
    while right - left > 1:
        candidate_size = left + (right - left) / 2
        if is_size_enough(candidate_size, count, width, height):
            right = candidate_size
        else:
            left = candidate_size

    min_acceptable_size = right
    return min_acceptable_size


def is_size_enough(size, count, width, height):
    cards_per_row = size // width
    cards_per_column = size // height
    return cards_per_row * cards_per_column >= count


def write_output(filename, size):
    with open(filename, "w") as output_file:
        output_file.write("%d" % size)


if __name__ == "__main__":
    main()
