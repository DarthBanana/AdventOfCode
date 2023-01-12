import os


def build_histogram(name):
    map = {}
    for c in name:
        if c == '[':
            break

        if c.isalpha():
            count = 0
            if c in map:
                count = map[c]

            map[c] = count + 1

    return list(map.items())


def get_checksum_field(name):
    return name[-6:-1]


def get_sector_id(name):
    return int(name[-10:-7])


def calc_checksum(name):
    histogram = build_histogram(name)
    histogram.sort(key=lambda x: (0-x[1], x[0]))

    checksum = ""
    for (x, v) in histogram[0:5]:
        checksum = checksum + x

    return checksum


def is_name_valid(name):
    return calc_checksum(name) == get_checksum_field(name)


def debug_solve(name):
    print("")
    print(name)
    print(calc_checksum(name))
    print(get_checksum_field(name))


def solve():
    result = 0
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + "\Day_4_input.txt"
    input_file = open(file_path, "r")
    count = 0
    for line in input_file.readlines():
        line = line.rstrip()
        debug_solve(line)
        if is_name_valid(line):
            result += get_sector_id(line)

    return result


print(get_checksum_field("aaaaa-bbb-z-y-x-123[abxyz]"))
print(build_histogram("aaaaa-bbb-z-y-x-123[abxyz]"))
print(get_sector_id("aaaaa-bbb-z-y-x-123[abxyz]"))
calc_checksum("aaaaa-bbb-z-y-x-123[abxyz]")
print(is_name_valid("aaaaa-bbb-z-y-x-123[abxyz]"))
print(is_name_valid("a-b-c-d-e-f-g-h-987[abcde]"))
print(is_name_valid("not-a-real-room-404[oarel]"))
print(is_name_valid("totally-real-room-200[decoy]"))
name = "rwcnawjcrxwju-snuuhknjw-jlzdrbrcrxw-979[rwjcn]"


print(solve())
