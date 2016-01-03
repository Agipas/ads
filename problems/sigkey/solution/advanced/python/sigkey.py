import sys


def main():
    input_filename = "sigkey.in" if len(sys.argv) == 1 else sys.argv[1]
    output_filename = "sigkey.out" if len(sys.argv) == 1 else sys.argv[2]

    keys = read_input(input_filename)
    key_pair_count = solve(keys)
    write_output(output_filename, key_pair_count)


def read_input(filename):
    with open(filename, "r") as input_file:
        count = int(input_file.readline())
        words = []
        for i in range(0, count):
            words.append(input_file.readline().strip())

        return words


def solve(keys):
    # For each key, we'll generate two 32-bit masks, where the bits represent the letters in the key.
    # For example, 'acef' corresponds to 0..0000110101 (the rightmost bit is 'a').
    # The second mask is the same but with all greater bits set to 1: 'acef' = 1..1111110101.
    #
    # We'll store both masks for each key in a hashtable.
    # Therefore, if two keys produce a pair, there is a pair of masks in the hashtable
    # whose bitwise AND operation produces all zeroes: 0..0000000000.
    #
    # This way, we can iterate over all positive masks (starting with zeroes),
    # and for each positive mask we'll look up its bitwise inverse in the hashtable.
    #
    # Example:
    #   'acef' and 'bd' produce a key pair.
    #   'acef' gives us two masks: 0..0000110101 and 1..1111110101.
    #     'bd' gives us two masks: 0..0000001010 and 1..1111111010.
    #
    #   For the mask 0..0000001010 there is a matching inverse mask 1..1111110101, so it's a key pair.

    key_set = set(produce_key_masks(keys))
    pair_count = len([
        True
        for bitmask in key_set
        if bitmask < (1 << 28) and (~bitmask & 0xFFFFFFFF) in key_set
    ])
    return pair_count


def produce_key_masks(keys):
    for key in keys:
        positive_mask, negative_mask = bitmasks(key)
        yield positive_mask
        yield negative_mask


def bitmasks(key):
    positive_mask = 0
    most_significant_bit = 0

    for char in key:
        bit_index = (ord(char) - 97)
        positive_mask |= (1 << bit_index)

        if bit_index > most_significant_bit:
            most_significant_bit = bit_index

    negative_mask = (~positive_mask ^ ((1 << most_significant_bit) - 1) | positive_mask) & 0xFFFFFFFF
    return positive_mask, negative_mask


def write_output(filename, key_pair_count):
    with open(filename, "w") as output_file:
        output_file.write("%d\n" % key_pair_count)


if __name__ == "__main__":
    main()
