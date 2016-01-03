import sys


alphabets = {
    chr(end_character_code): map(chr, range(ord('a'), end_character_code + 1))
    for end_character_code in range(ord('a'), ord('z') + 1)
}

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
    key_set = {
        ''.join(sorted(key))
        for key in keys
    }
    return len([
        True
        for public_key in key_set
        if private_key(public_key) in key_set
    ])


def private_key(public_key):
    alphabet = alphabets[public_key[-1]]
    return ''.join([char for char in alphabet if char not in public_key])


def write_output(filename, key_pair_count):
    with open(filename, "w") as output_file:
        output_file.write("%d\n" % key_pair_count)


if __name__ == "__main__":
    main()
