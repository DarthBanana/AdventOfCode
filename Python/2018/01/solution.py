## advent of code 2018
## https://adventofcode.com/2018
## day 01

import parsehelp
class Puzzle:
    def __init__(self, lines):
        self.always_run_part_1 = False        
        print(lines)
        self.data = parsehelp.get_int_per_line(lines)

    def part1(self):
        value = 0
        for num in self.data:
            value += num
        return value
        

    def part2(self):
        pass