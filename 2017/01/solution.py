## advent of code 2017
## https://adventofcode.com/2017
## day 01


def parse_input(lines):
    return lines[0]


def part1(data):
    sum = 0
    for i in range(len(data)):
        other = (i + 1) % len(data)
        if data[i] == data[other]:
            sum += int(data[i])
    return sum


def part2(data):
    sum = 0
    for i in range(len(data)):
        other = (i + len(data) // 2) % len(data)
        if data[i] == data[other]:
            sum += int(data[i])
    return sum
