import os
import re

swap_pos_re = re.compile(r"swap position (\d+) with position (\d+)")
swap_let_re = re.compile(r"swap letter (\w) with letter (\w)")
rotate_re = re.compile(r"rotate (\w+) (\d+) step")
rotate_pos_re = re.compile(r"rotate based on position of letter (\w)")
reverse_sub_re = re.compile(r"reverse positions (\d+) through (\d+)")
move_re = re.compile(r"move position (\d+) to position (\d+)")


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


def swap_position(string, x, y):
    first = min(x, y)
    second = max(x, y)
    new_string = string[0:first] + string[second] + \
        string[first + 1:second] + string[first] + string[second + 1:]

    return new_string


def swap_letters(string, x, y):
    new_string = ""
    for c in string:
        if c == x:
            new_string += y
        elif c == y:
            new_string += x
        else:
            new_string += c

    return new_string


def rotate(string, direction, steps):
    steps = steps % len(string)
    if direction == "right":
        steps = steps * -1

    new_start = (len(string) + steps) % len(string)

    new_string = string[new_start:] + string[0:new_start]

    return new_string


def rotate_based_on_postion(string, letter):
    index = re.search(letter, string).span()[0]
    steps = 1 + index
    if index >= 4:
        steps += 1

    return rotate(string, "right", steps)


def reverse_substring(string, start, end):
    substring = string[start:end + 1]
    reversed_substring = "".join(reversed(substring))
    new_string = string[0:start] + reversed_substring + string[end+1:]
    return new_string


def move(string, from_index, to_index):
    new_string = string[0:from_index] + string[from_index + 1:]
    new_string = new_string[0:to_index] + \
        string[from_index] + new_string[to_index:]

    return new_string


def execute_instruction(line, string):

    if match := swap_pos_re.search(line):
        string = swap_position(string, int(
            match.groups()[0]), int(match.groups()[1]))
    elif match := swap_let_re.search(line):
        string = swap_letters(string, match.groups()[0], match.groups()[1])
    elif match := rotate_re.search(line):
        string = rotate(string, match.groups()[0], int(match.groups()[1]))
    elif match := rotate_pos_re.search(line):
        string = rotate_based_on_postion(string, match.groups()[0])
    elif match := reverse_sub_re.search(line):
        string = reverse_substring(string, int(
            match.groups()[0]), int(match.groups()[1]))
    elif match := move_re.search(line):
        string = move(string, int(match.groups()[0]), int(match.groups()[1]))
    else:
        print("!!!!! ", line)
        assert (False)

    return string


def execute(filename, string):
    file = open_file(filename)

    for line in file.readlines():
        print(string)
        print(line)
        string = execute_instruction(line, string)

    return string


def test(instruction, string, expected):
    result = execute_instruction(instruction, string)
    print(result)
    assert (result == expected)


print(swap_position("abcde", 4, 0))
print(swap_letters("ebcda", "d", "b"))
print(reverse_substring("edcba", 0, 4))

print(execute("test.txt", "abcde"))

print("Result for part 1 : ", execute("input.txt", "abcdefgh"))
