import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


def decompress(compressed_text):
    print(compressed_text)

    marker = re.compile(r"\((\d+)x(\d+)\)")
    new_string = compressed_text
    last_index = 0
    while (True):
        match = marker.search(new_string[last_index:])
        if match == None:
            print(len(new_string))
            print(calc_decompress_len(compressed_text))
            assert len(new_string) == calc_decompress_len(compressed_text)
            return new_string
        match_start = last_index + match.span()[0]
        match_end = last_index + match.span()[1]

        temp_string = new_string[0:match_start]

        repeat_length = int(match.group(1))
        repeat_count = int(match.group(2))
        for i in range(repeat_count):
            temp_string += new_string[match_end:match_end + repeat_length]

        last_index = match_start
        temp_string += new_string[match_end + repeat_length:]
        new_string = temp_string


def calc_decompress_len(compressed_text):
    marker = re.compile(r"\((\d+)x(\d+)\)")
    match = marker.search(compressed_text)
    if match == None:
        return len(compressed_text)
    match_start = match.span()[0]
    match_end = match.span()[1]
    repeat_length = int(match.group(1))
    repeat_count = int(match.group(2))
    print(compressed_text)
    length = match_start
    print(length)
    length += calc_decompress_len(
        compressed_text[match_end:match_end + repeat_length]) * repeat_count
    print(length)
    length += calc_decompress_len(compressed_text[match_end+repeat_length:])

    return length


def test():

    assert decompress("(3x3)XYZ") == "XYZXYZXYZ"

    assert decompress("X(8x2)(3x3)ABCY") == "XABCABCABCABCABCABCY"
    assert calc_decompress_len("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
    assert calc_decompress_len(
        "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445


def run():
    file = open_file("input.txt")
    data = file.readline()
    result = calc_decompress_len(data)
    return result


test()

print(run())
