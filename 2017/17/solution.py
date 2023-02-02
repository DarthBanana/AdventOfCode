## advent of code 2017
## https://adventofcode.com/2017
## day 17

from collections import deque


class Puzzle:
    def __init__(self, lines):
        self.step = int(lines[0])
        self.reset()

    def reset(self):
        self.circular_buffer = deque([0])
        self.index = 1

    def next_step(self):
        self.circular_buffer.rotate(-1 * self.step)
        self.circular_buffer.append(self.index)
        self.index += 1

    def execute_steps(self, count):
        for i in range(count):
            self.next_step()

    def get_value_after(self, value):
        index = self.circular_buffer.index(value) + 1
        index = index % len(self.circular_buffer)
        return self.circular_buffer[index]

    def simulate_steps(self, count):
        index = 0
        length = 1
        num_after = 0
        for i in range(1, count + 1):
            index = (index + self.step) % length + 1
            if index == 1:
                num_after = i
            length += 1
        return num_after


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.execute_steps(2017)
    return puzzle.get_value_after(2017)


def part2(puzzle):
    return puzzle.simulate_steps(50000000)
