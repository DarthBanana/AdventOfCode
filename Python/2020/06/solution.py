## advent of code 2020
## https://adventofcode.com/2020
## day 06

from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)

    def part1(self):
        groups = []
        group = set()
        for line in self.lines:
            if line == '':
                groups.append(group)
                group = set()
            else:
                for c in line:
                    group.add(c)

        groups.append(group)

        return sum(len(g) for g in groups)

    def part2(self):
        groups = []
        group = set('abcdefghijklmnopqrstuvwxyz')
        for line in self.lines:
            if line == '':
                groups.append(group)
                group = set('abcdefghijklmnopqrstuvwxyz')
            else:
                group = group.intersection(set(line))

        groups.append(group)
        return sum(len(g) for g in groups)
        