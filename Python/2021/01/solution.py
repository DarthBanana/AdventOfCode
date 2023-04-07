## advent of code 2021
## https://adventofcode.com/2021
## day 01

from aocpuzzle import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.readings = get_int_per_line(lines)

    def part1(self):
        last = self.readings[0]
        count = 0
        for reading in self.readings[1:]:
            if reading > last:
                count += 1
            last = reading
        return count        

    def part2(self):
        windows = [sum(self.readings[i:i+3]) for i in range(len(self.readings)-2)]
        last = windows[0]
        count = 0
        for reading in windows[1:]:
            if reading > last:
                count += 1
            last = reading
        return count  