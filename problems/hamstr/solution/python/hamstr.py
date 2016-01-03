import sys


def main():
    input_filename = "hamstr.in" if len(sys.argv) == 1 else sys.argv[1]
    output_filename = "hamstr.out" if len(sys.argv) == 1 else sys.argv[2]

    supplies, hamsters = read_input(input_filename)
    max_hamsters = solve(supplies, hamsters)
    write_output(output_filename, max_hamsters)


def read_input(filename):
    with open(filename, "r") as input_file:
        supplies = int(input_file.readline())
        hamster_count = int(input_file.readline())

        hamsters = []
        for i in range(0, hamster_count):
            hamster = [int(hamster_str) for hamster_str in input_file.readline().split()]
            hamsters.append(hamster)

        return supplies, hamsters


def solve(supplies, hamsters):
    # Using binary search over the possible number of hamsters to buy.
    # This gives us an overall complexity of O(C * log C * log C).
    # [O(log C) for searching, O(C * log C) for sorting on each iteration]
    possible_hamster_counts = range(0, len(hamsters))
    comparator = lambda hamster_count: get_required_food_for_best_k_hamsters(hamsters, k=hamster_count) > supplies
    max_affordable_hamsters = binary_search_rightmost(possible_hamster_counts, comparator)
    return max_affordable_hamsters


def binary_search_rightmost(sorted_data, comparator, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(sorted_data)
        
    while left < right:
        # Adding + 1 here and checking for ">" ensures that we find the rightmost element among equals.
        # If we wanted the leftmost one, it would be:
        # (left + right) / 2, "<" comparison, left = middle + 1, right = middle.
        middle = (left + right + 1) / 2
        if comparator(middle) > 0:
            right = middle - 1
        else:
            left = middle

    return right


def get_required_food_for_best_k_hamsters(hamsters, k):
    required_food_per_hamster = [
        hunger + greed * (k - 1)
        for hunger, greed in hamsters
    ]
    sort(required_food_per_hamster)
    required_food = sum(required_food_per_hamster[:k])
    return required_food


def sort(array):
    merge_results = [0] * len(array)
    merge_sort_recursive(array, merge_results, 0, len(array) - 1)


def merge_sort_recursive(array, merge_results, left, right):
    if left < right:
        middle = (left + right) // 2
        merge_sort_recursive(array, merge_results, left, middle)
        merge_sort_recursive(array, merge_results, middle + 1, right)
        merge(array, merge_results, left, middle + 1, right)


def merge(array, merge_results, left_begin, right_begin, right_end):
    left_end = right_begin - 1
    left_read_pos = left_begin
    right_read_pos = right_begin
    result_write_pos = left_begin

    while left_read_pos <= left_end and right_read_pos <= right_end:
        if array[left_read_pos] < array[right_read_pos]:
            merge_results[result_write_pos] = array[left_read_pos]
            left_read_pos += 1
        else:
            merge_results[result_write_pos] = array[right_read_pos]
            right_read_pos += 1
        result_write_pos += 1

    while left_read_pos <= left_end:
        merge_results[result_write_pos] = array[left_read_pos]
        left_read_pos += 1
        result_write_pos += 1

    while right_read_pos <= right_end:
        merge_results[result_write_pos] = array[right_read_pos]
        right_read_pos += 1
        result_write_pos += 1

    array[left_begin:right_end + 1] = merge_results[left_begin:right_end + 1]


def write_output(filename, max_hamsters):
    with open(filename, "w") as output_file:
        output_file.write("%d" % max_hamsters)


if __name__ == "__main__":
    main()
