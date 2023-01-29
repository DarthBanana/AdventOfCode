## advent of code 2017
## https://adventofcode.com/2017
## day 02

import re
import itertools


def parse_input(lines):
    num_re = re.compile(r"(\d+)")
    rows = []
    for line in lines:
        row = []
        for match in num_re.finditer(line):
            row.append(int(match.group(1)))
        rows.append(row)
    return rows


def part1(data):
    checksum = 0
    for row in data:
        checksum += max(row) - min(row)
    return checksum


def part2(data):
    checksum = 0
    for row in data:
        combos = itertools.combinations(row, 2)
        for combo in list(combos):
            sort = sorted(combo)
            if sort[1] % sort[0] == 0:
                checksum += sort[1] // sort[0]
                break
    return checksum
