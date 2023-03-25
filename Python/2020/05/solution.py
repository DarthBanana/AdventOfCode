## advent of code 2020
## https://adventofcode.com/2020
## day 05

from aocpuzzle import *
class BoardingPass():
    def __init__(self, line):
        self.line = line
        self.row = 0
        self.col = 0
        self.seat_id = 0
        for i in range(7):
            if self.line[i] == 'B':
                self.row += 2**(6-i)
        for i in range(7, 10):
            if self.line[i] == 'R':
                self.col += 2**(9-i)
        self.seat_id = self.row * 8 + self.col

    
    
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.boarding_passes = []
        for line in lines:
            self.boarding_passes.append(BoardingPass(line))

    def part1(self):
        return max([boarding_pass.seat_id for boarding_pass in self.boarding_passes])

    def part2(self):
        ids = [boarding_pass.seat_id for boarding_pass in self.boarding_passes]
        ids.sort()
        for i in range(len(ids)-1):
            if ids[i+1] - ids[i] == 2:
                return ids[i] + 1