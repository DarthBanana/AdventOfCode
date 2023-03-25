## advent of code 2020
## https://adventofcode.com/2020
## day 02

import re
from aocpuzzle import *

input_re = re.compile(r'(\d+)-(\d+) (\w): (\w+)')

class Password:
    def __init__(self, line):
        self.min, self.max, self.char, self.password = input_re.match(line).groups()
        self.min = int(self.min)
        self.max = int(self.max)
    def is_valid(self):
        return self.min <= self.password.count(self.char) <= self.max
    
    def is_valid_2(self):
        return (self.password[self.min-1] == self.char) != (self.password[self.max-1] == self.char)

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.passwords = [Password(line) for line in lines]

    def part1(self):
        valid_count = 0
        for password in self.passwords:
            if password.is_valid():
                valid_count += 1
        return valid_count

    def part2(self):
        valid_count = 0
        for password in self.passwords:
            if password.is_valid_2():
                valid_count += 1
        return valid_count