## advent of code 2017
## https://adventofcode.com/2017
## day 22
from enum import Enum


UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def add_em(a, b):
    return tuple(x + y for x, y in zip(a, b))


class State(Enum):
    CLEAN = 1
    WEAKENED = 2
    INFECTED = 3
    FLAGGED = 4


class Puzzle:
    def __init__(self, lines):
        self.original_map = {}
        y = 0
        max_x = 0

        for line in lines:
            x = 0
            for c in line:
                if c == "#":
                    self.original_map[(x, y)] = State.INFECTED
                x += 1
            max_x = x
            y += 1

        self.original_maxes = (max_x - 1, y - 1)

        start_x = (max_x - 1) / 2
        start_y = (y - 1) / 2
        self.start = (int(start_x), int(start_y))
        self.reset()
        print(self.start)

    def reset(self):
        self.map = self.original_map.copy()
        self.current = self.start
        self.direction_index = 0
        self.infection_count = 0
        self.min_pos = (0, 0)
        self.max_pos = self.original_maxes

    def print(self):
        print()
        print("Map:")
        for y in range(self.min_pos[1], self.max_pos[1] + 1):
            for x in range(self.min_pos[0], self.max_pos[0] + 1):
                pos = (x, y)
                if pos == self.current:
                    print("[", end="")
                else:
                    print(" ", end="")

                if pos in self.map.keys():
                    state = self.map[pos]
                    if state == State.WEAKENED:
                        print("W", end="")
                    elif state == State.FLAGGED:
                        print("F", end="")
                    elif state == State.INFECTED:
                        print("#", end="")
                    else:
                        assert False
                else:
                    print(".", end="")

                if pos == self.current:
                    print("]", end="")
                else:
                    print(" ", end="")

            print()

    def turn_right(self):
        self.direction_index = (self.direction_index + 1) % len(DIRECTIONS)

    def turn_left(self):
        self.direction_index = (self.direction_index + len(DIRECTIONS) - 1) % len(
            DIRECTIONS
        )

    def reverse(self):
        self.direction_index = (self.direction_index + 2) % len(DIRECTIONS)

    def move_forward(self):
        dir = DIRECTIONS[self.direction_index]
        self.current = add_em(self.current, dir)
        self.min_pos = (
            min(self.current[0], self.min_pos[0]),
            min(self.current[1], self.min_pos[1]),
        )
        self.max_pos = (
            max(self.current[0], self.max_pos[0]),
            max(self.current[1], self.max_pos[1]),
        )

    def step(self):
        if self.current in self.map.keys():
            self.turn_right()
            self.map.pop(self.current)
        else:
            self.turn_left()
            self.map[self.current] = State.INFECTED
            self.infection_count += 1
        self.move_forward()

    def step2(self):
        if not (self.current in self.map.keys()):
            # CLEAN
            self.map[self.current] = State.WEAKENED
            self.turn_left()
        else:
            state = self.map[self.current]
            if state == State.WEAKENED:
                self.map[self.current] = State.INFECTED
                self.infection_count += 1
            elif state == State.INFECTED:
                self.map[self.current] = State.FLAGGED
                self.turn_right()
            elif state == State.FLAGGED:
                self.map[self.current] = State.CLEAN
                self.map.pop(self.current)
                self.reverse()
            else:
                assert False
        self.move_forward()

    def run(self, steps):
        for i in range(steps):
            self.step()

    def run2(self, steps):
        for i in range(steps):
            self.step2()


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.run(10000)
    return puzzle.infection_count


def part2(puzzle):
    puzzle.reset()
    puzzle.run2(10000000)
    return puzzle.infection_count
