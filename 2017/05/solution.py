## advent of code 2017
## https://adventofcode.com/2017
## day 05


def parse_input(lines):
    instructions = []
    for line in lines:
        instructions.append(int(line))
    return instructions


def part1(data):
    instructions = data.copy()
    ip = 0
    steps = 0
    while 0 <= ip < len(instructions):
        steps += 1
        offset = instructions[ip]
        instructions[ip] += 1
        ip = ip + offset
    return steps


def part2(data):
    instructions = data.copy()
    ip = 0
    steps = 0
    while 0 <= ip < len(instructions):
        steps += 1
        offset = instructions[ip]
        if offset >= 3:
            instructions[ip] -= 1
        else:
            instructions[ip] += 1
        ip = ip + offset
    return steps
