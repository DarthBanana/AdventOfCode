## advent of code 2017
## https://adventofcode.com/2017
## day 06


def parse_input(lines):
    blocks = []
    for value in lines[0].split():
        blocks.append(int(value))
    return blocks


def part1(data):
    banks = data.copy()
    history = set()
    history.add(tuple(banks))
    steps = 0
    while True:
        steps += 1
        max_index = 0
        max_number = 0
        for index, number in enumerate(banks):
            if number > max_number:
                max_index = index
                max_number = number
        blocks = banks[max_index]
        banks[max_index] = 0
        next_index = max_index
        while blocks:
            next_index += 1
            next_index = next_index % len(banks)
            banks[next_index] += 1
            blocks -= 1
        hash = tuple(banks)
        if hash in history:
            return steps
        history.add(hash)


def get_cycle_state(data):
    banks = data.copy()
    history = set()
    history.add(tuple(banks))
    steps = 0
    while True:
        steps += 1
        max_index = 0
        max_number = 0
        for index, number in enumerate(banks):
            if number > max_number:
                max_index = index
                max_number = number
        blocks = banks[max_index]
        banks[max_index] = 0
        next_index = max_index
        while blocks:
            next_index += 1
            next_index = next_index % len(banks)
            banks[next_index] += 1
            blocks -= 1
        hash = tuple(banks)
        if hash in history:
            return banks
        history.add(hash)


def part2(data):
    banks = get_cycle_state(data)
    return part1(banks)
