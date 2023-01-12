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


def get_substring(name):
    return name[0:-11]


def is_name_valid(name):
    return calc_checksum(name) == get_checksum_field(name)


def debug_solve(name):
    print("")
    print(name)
    print(calc_checksum(name))
    print(get_checksum_field(name))


def decrypt(name):
    sub_name = get_substring(name)
    id = get_sector_id(name) % 26
    room_name = ""
    for c in sub_name:
        if c == '-':
            room_name += ' '
            continue

        c_offset = ord(c) - ord('a')
        new_offset = (c_offset + id) % 26
        new_c_code = new_offset + ord('a')
        new_c = chr(new_c_code)
        room_name += new_c
    return room_name


def solve():

    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + "\Day_4_input.txt"
    input_file = open(file_path, "r")
    count = 0
    for line in input_file.readlines():
        line = line.rstrip()
        if is_name_valid(line):

            room = decrypt(line)
            if "orth" in room:
                print("")
                print(line)
                print(room)


name = "aaaaa-bbb-z-y-x-123[abxyz]"
print(get_substring(name))
name = "qzmt-zixmtkozy-ivhz-343[aaaaa]"
print(decrypt(name))

solve()
