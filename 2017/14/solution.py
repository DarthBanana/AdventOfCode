## advent of code 2017
## https://adventofcode.com/2017
## day 14

from collections import deque
import itertools

NUM_ONES = {
    "0": 0,
    "1": 1,
    "2": 1,
    "3": 2,
    "4": 1,
    "5": 2,
    "6": 2,
    "7": 3,
    "8": 1,
    "9": 2,
    "a": 2,
    "b": 3,
    "c": 2,
    "d": 3,
    "e": 3,
    "f": 4,
}
NEIGHBORS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def add_coord(a, b):
    return (a[0] + b[0], a[1] + b[1])


def convert_data(data):
    input = []
    tail = [17, 31, 73, 47, 23]
    for c in data:
        input.append(ord(c))
    return input + tail


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


def calculate_hash(data):
    input = convert_data(data)
    list = deque(range(256))
    skip_size = 0
    start = 0
    for i in range(64):
        list, start, skip_size = hash(input, list, start, skip_size)

    dense = dense_hash(list)
    return dense


class Puzzle:
    def __init__(self, lines):
        self.text = lines[0]
        self.squares = set()
        self.groups = []
        self.current_group = set()

    def build_hashes(self):
        self.hashes = []
        self.one_count = 0

        for i in range(128):
            input = self.text + "-"
            input = input + str(i)
            hash = calculate_hash(input)
            self.one_count += count_ones(hash)
            self.hashes.append(convert_to_binary(hash))

    def get_squares(self):
        self.squares = set()
        for row in range(128):
            bin = self.hashes[row]
            for col in range(128):
                if bin[col] == "1":
                    self.squares.add((col, row))

    def find_group(self, start):
        if start in self.current_group:
            return
        self.current_group.add(start)

        for n in NEIGHBORS:
            next = add_coord(start, n)
            if next in self.squares:
                self.find_group(next)

    def get_groups(self):
        self.groups = []
        unvisited = self.squares.copy()
        while len(unvisited):
            self.current_group = set()
            start = unvisited.pop()
            self.find_group(start)
            self.groups.append(self.current_group)
            unvisited = unvisited - self.current_group


def count_ones(hash):
    count = 0
    for c in hash:
        count += NUM_ONES[c]
    return count


def convert_to_binary(hash):
    return f"{int(hash, 16):0>128b}"


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.build_hashes()
    return puzzle.one_count


def part2(puzzle):
    puzzle.get_squares()
    puzzle.get_groups()
    return len(puzzle.groups)
