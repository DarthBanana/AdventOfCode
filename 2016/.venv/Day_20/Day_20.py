import os
import re
TEST_RANGES = [(5, 8), (0, 2), (4, 7)]
MAX_IP = 4294967295


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


def get_ranges_from_file(filename):
    ranges = []
    nums_re = re.compile(r"(\d+)-(\d+)")

    file = open_file(filename)
    for line in file.readlines():
        match = nums_re.search(line)
        start = int(match.groups()[0])
        end = int(match.groups()[1])
        ranges.append((start, end))

    return ranges


def find_first_valid_address(ranges):
    ranges.sort(key=lambda val: val[0])
    starting_range = (0, 0)
    for range in ranges:
        if range[0] > starting_range[1] + 1:
            return starting_range[1] + 1
        starting_range = (starting_range[0], max(starting_range[1], range[1]))


def count_all_valid_addresses(ranges, max_val):
    ranges.sort(key=lambda val: val[0])
    count = 0
    starting_range = (0, 0)
    for range in ranges:
        if range[0] > starting_range[1] + 1:
            count += range[0] - (starting_range[1] + 1)
            starting_range = range
            continue

        starting_range = (starting_range[0], max(starting_range[1], range[1]))

    count += max_val - starting_range[1]
    return count


def test(input, expected):
    result = find_first_valid_address(input)
    print(result)
    assert (result == expected)


def test2(input, max, expected):
    result = count_all_valid_addresses(input, max)
    print(result)
    assert (result == expected)


test(TEST_RANGES, 3)
test2(TEST_RANGES, 9, 2)
real_input = get_ranges_from_file("input.txt")

print("Part 1 result: ", find_first_valid_address(real_input))
print("Part 2 result: ", count_all_valid_addresses(real_input, MAX_IP))
