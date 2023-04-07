## advent of code 2021
## https://adventofcode.com/2021
## day 02

from aocpuzzle import *
from PrettyMap2D import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)

    def part1(self):
        x = 0
        depth = 0        
        for line in self.lines:
            if line[0] == "f":
                x += int(line[8])
            elif line[0] == "u":
                depth -= int(line[3])
                assert(depth >= 0)
            elif line[0] == "d":
                depth += int(line[5])
            else:
                assert(False)
        return x * depth
    def part2(self):
        x = 0
        depth = 0
        aim = 0
        for line in self.lines:
            if line[0] == "f":
                dist = int(line[8])
                x += dist
                depth += aim * dist
                assert(depth >= 0)

            elif line[0] == "u":
                aim -= int(line[3])
                assert(depth >= 0)
            elif line[0] == "d":
                aim += int(line[5])
            else:
                assert(False)
        return x * depth        

        pass