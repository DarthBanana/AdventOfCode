## advent of code 2017
## https://adventofcode.com/2017
## day 12
class Program:
    def __init__(self, line):
        split = line.split(" <-> ")
        self.index = int(split[0])
        self.connected_to = []
        for c in split[1].split(", "):
            self.connected_to.append(int(c))


class Puzzle:
    def __init__(self, lines):
        self.programs = {}
        for line in lines:
            program = Program(line)
            self.programs[program.index] = program

    def find_all(self, index):
        if index in self.seen:
            return
        self.seen.add(index)
        program = self.programs[index]
        for c in program.connected_to:
            self.find_all(c)

    def find_all_connected_to_zero(self):
        self.seen = set()
        self.find_all(0)

    def find_all_groups(self):
        not_grouped = set(self.programs.keys())
        groups = []
        while len(not_grouped):
            self.seen = set()
            start = not_grouped.pop()
            self.find_all(start)
            groups.append(self.seen.copy())
            not_grouped = not_grouped - self.seen
        return len(groups)


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.find_all_connected_to_zero()
    return len(puzzle.seen)


def part2(puzzle):
    return puzzle.find_all_groups()
