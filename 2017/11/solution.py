## advent of code 2017
## https://adventofcode.com/2017
## day 11

N = (0, -2)
NE = (1, -1)
SE = (1, 1)
S = (0, 2)
SW = (-1, 1)
NW = (-1, -1)


def parse_input(lines):
    steps = []
    for d in lines[0].split(","):
        if d == "n":
            steps.append(N)
        elif d == "ne":
            steps.append(NE)
        elif d == "se":
            steps.append(SE)
        elif d == "s":
            steps.append(S)
        elif d == "sw":
            steps.append(SW)
        elif d == "nw":
            steps.append(NW)
        else:
            assert False
    return steps


def add_coord(a, b):
    return (a[0] + b[0], a[1] + b[1])


def calc_distance(a, b):
    dcol = abs(a[0] - b[0])
    drow = abs(a[1] - b[1])
    return dcol + max(0, (drow - dcol) // 2)


def part1(data):
    position = (0, 0)
    for step in data:
        position = add_coord(position, step)

    return calc_distance((0, 0), position)


def part2(data):
    position = (0, 0)
    farthest = 0
    for step in data:
        position = add_coord(position, step)
        farthest = max(farthest, calc_distance((0, 0), position))
    return farthest
