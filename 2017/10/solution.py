## advent of code 2017
## https://adventofcode.com/2017
## day 10

from collections import deque
import itertools


def parse_input(lines):
    return lines[0]


def hash(input, list, start, skip_size):
    list.rotate(-1 * start)
    for num in input:
        sublista = deque(itertools.islice(list, num))
        sublistb = deque(itertools.islice(list, num, len(list)))
        sublista.reverse()
        list = sublista + sublistb
        distance = num + skip_size
        start += distance
        list.rotate(-1 * (num + skip_size))
        skip_size += 1
    list.rotate(start)
    return (list, start, skip_size)


def convert_part1_data(data):
    input = []
    for m in data.split(","):
        input.append(int(m))
    return input


def part1(data):
    input = convert_part1_data(data)
    list = deque(range(256))
    list, _, _ = hash(input, list, 0, 0)
    return list[0] * list[1]


def convert_part2_data(data):
    input = []
    tail = [17, 31, 73, 47, 23]
    for c in data:
        input.append(ord(c))
    return input + tail


def dense_hash(sparse_hash):
    dense_hash = []
    for set_start in range(0, len(sparse_hash), 16):
        value = 0
        for i in range(0, 16):
            value = value ^ sparse_hash[i + set_start]
        dense_hash.append(value)
    string = ""
    for val in dense_hash:
        string += f"{val:0>2x}"
    return string


def part2(data):
    input = convert_part2_data(data)
    list = deque(range(256))
    skip_size = 0
    start = 0
    for i in range(64):
        list, start, skip_size = hash(input, list, start, skip_size)

    dense = dense_hash(list)
    return dense
