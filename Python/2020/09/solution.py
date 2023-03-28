## advent of code 2020
## https://adventofcode.com/2020
## day 09

from aocpuzzle import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.data = get_int_per_line(lines)
        if is_test:
            self.preamble_length = 5
        else:
            self.preamble_length = 25
        self.invalid_number = None
        self.always_run_part_1 = True

    def part1(self):
        for i in range(self.preamble_length, len(self.data)):
            preamble = self.data[i-self.preamble_length:i]
            target = self.data[i]
            found = False
            for j in range(len(preamble)):
                for k in range(j+1, len(preamble)):
                    if preamble[j] + preamble[k] == target:
                        found = True
                        break
                if found:
                    break
            if not found:
                self.invalid_number = target
                return target

    

    def part2(self):
        for i in range(len(self.data)):
            for j in range(i+1, len(self.data)):
                series_sum = sum(self.data[i:j])

                if series_sum == self.invalid_number:
                    return min(self.data[i:j]) + max(self.data[i:j])
                elif series_sum > self.invalid_number:
                    break
                