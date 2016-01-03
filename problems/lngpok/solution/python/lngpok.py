import sys


def main():
    input_filename = "lngpok.in" if len(sys.argv) == 1 else sys.argv[1]
    output_filename = "lngpok.out" if len(sys.argv) == 1 else sys.argv[2]

    cards = read_input(input_filename)
    max_sequence_length = solve(cards)
    write_output(output_filename, max_sequence_length)


def read_input(filename):
    with open(filename, "r") as input_file:
        cards = [int(card_str) for card_str in input_file.readline().split()]
        return cards


def solve(cards):
    sort(cards)
    joker_count = count_jokers(cards)
    uniques = get_unique_non_jokers(cards)

    result = find_max_sequence_length(uniques, joker_count) + joker_count
    return result


def count_jokers(sorted_cards):
    for i in range(0, len(sorted_cards)):
        if sorted_cards[i] != 0:
            return i
    return len(sorted_cards)


def get_unique_non_jokers(sorted_cards):
    result = []
    current_card = 0
    for card in sorted_cards:
        if card != current_card:
            result.append(card)
            current_card = card
    return result


def find_max_sequence_length(uniques, joker_budget):
    # Find the largest segment [i, j] for which 'get_joker_cost(i, j)' does not exceed 'joker_budget'.

    max_length = 0
    last = len(uniques) - 1
    search_space = range(0, last + 1)

    for i in search_space:

        # We could just do a simple loop from 'last' down to 'i', but that would give us O(N^2).
        # Instead, we'll use binary search here to locate the right bound in O(log N).
        # Therefore, the total complexity for search would be O(N) * O(log N) = O(N log N).
        comparator = lambda right_bound: get_joker_cost(uniques, i, right_bound) > joker_budget
        max_allowed_right_bound = binary_search_rightmost(search_space, comparator, left=i, right=last)

        max_length_starting_from_i = max_allowed_right_bound - i + 1
        max_length = max(max_length, max_length_starting_from_i)

    return max_length


def get_joker_cost(uniques, left, right):
    return uniques[right] - uniques[left] + 1 - (right - left + 1)


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


def write_output(filename, max_sequence_length):
    with open(filename, "w") as output_file:
        output_file.write("%d" % max_sequence_length)


if __name__ == "__main__":
    main()
