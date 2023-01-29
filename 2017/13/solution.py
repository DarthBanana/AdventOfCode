## advent of code 2017
## https://adventofcode.com/2017
## day 13

import re


def parse_input(lines):
    input_re = re.compile(r"(\d*): (\d*)")
    layers = []
    for line in lines:
        match = input_re.search(line)
        layers.append((int(match.group(1)), int(match.group(2))))
    return layers


def part1(data):
    sum = 0
    for depth, range in data:
        if depth % (range * 2 - 2) == 0:
            sum += depth * range
    return sum


def will_pass(data, time):
    for depth, range in data:
        if (time + depth) % (range * 2 - 2) == 0:
            return False
    return True


def part2(data):
    time = 0
    while not will_pass(data, time):
        time += 1

    return time
