## advent of code 2020
## https://adventofcode.com/2020
## day 01

from parsehelp import *
from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.expenses = get_int_per_line(lines)
    def part1(self):
        for e in self.expenses:
            other = 2020 - e
            if other in self.expenses:
                return e * other
        pass

    def part2(self):
        for i in range(len(self.expenses)-2):
            for j in range(i+1, len(self.expenses)-1):
                sum = self.expenses[i] + self.expenses[j]
                if sum > 2020:
                    continue
                remainder = 2020 - sum
                if remainder in self.expenses[j+1:]:
                    return self.expenses[i] * self.expenses[j] * remainder