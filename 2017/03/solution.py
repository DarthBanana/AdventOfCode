## advent of code 2017
## https://adventofcode.com/2017
## day 03


def parse_input(lines):
    return int(lines[0])


def part1(data):
    # concentric rings
    # n0 = (0,0)
    # ring0 = (0,0)(0,0)
    # ringN+1 = (RingN.minX - 1, RingN.minY - 1), (RingN.maxX + 1, RingN.maxY + 1
    # CircumferenceN+1 = 4*widthN + 4)
    # ring dimensions
    # n+1 width = n width + 2

    # n+1 layer_length = n+1 width *2 + (n width) * 2
    # n+1 start = (n_start.y + n_width
    ring = 0
    ring_range = range(1, 2)
    ring_width = 1
    min_val = 1
    max_val = 1
    starting_position = (0, 0)
    ending_position = (0, 0)
    while not (data in range(min_val, max_val + 1)):
        ring += 1
        min_val = max_val + 1
        circumference = ring_width * 4 + 4
        max_val = min_val + circumference - 1
        ring_width += 2

        starting_position = (ending_position[0] + 1, ending_position[1])
        ending_position = (starting_position[0], starting_position[1] + 1)
    # Found the ring, now find the position
    bottom_right_position = ending_position
    top_right_position = (
        bottom_right_position[0],
        bottom_right_position[1] - (ring_width - 1),
    )
    top_left_position = (
        top_right_position[0] - (ring_width - 1),
        top_right_position[1],
    )
    bottom_left_position = (
        top_left_position[0],
        top_left_position[0] + (ring_width - 1),
    )

    bottom_right = max_val
    top_right = min_val + (ring_width - 2)
    top_left = top_right + (ring_width - 1)
    bottom_left = top_left + (ring_width - 1)
    if data <= top_right:
        delta = top_right - data
        position = (top_right_position[0], top_right_position[1] + delta)
    elif data <= top_left:
        delta = top_left - data
        position = (top_left_position[0] + delta, top_left_position[1])
    elif data <= bottom_left:
        delta = bottom_left - data
        position = (bottom_left_position[0], bottom_left_position[1] - delta)
    elif data <= bottom_right:
        delta = bottom_right - data
        position = (bottom_right_position[0] - delta, bottom_right_position[1])
    else:
        assert False
    print(position)
    return abs(position[0]) + abs(position[1])


def add_coord(a, b):
    return (a[0] + b[0], a[1] + b[1])


NEIGHBORS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)

map = {}


def calc_value(position):
    value = 0
    for neighbor in NEIGHBORS:
        next = add_coord(neighbor, position)
        if next in map:
            value += map[next]
    map[position] = value
    return value


def position_iter():
    width = 1
    map[(0, 0)] = 1
    position = (1, 0)
    map[position] = 1

    while True:
        # UP
        for i in range(width):

            position = add_coord(position, UP)
            yield position
        width += 1
        # LEFT
        for i in range(width):
            position = add_coord(position, LEFT)
            yield position
        # DOWN
        for i in range(width):
            position = add_coord(position, DOWN)
            yield position
        width += 1
        # RIGHT
        for i in range(width):
            position = add_coord(position, RIGHT)
            yield position


def part2(data):

    width = 3
    map[(0, 0)] = 1
    position = (1, 0)
    map[position] = 1
    while True:
        # UP
        for position in position_iter():
            value = calc_value(position)
            if value > data:
                return value
