## advent of code 2018
## https://adventofcode.com/2018
## day 03
import re
import sys

from Map2D import * 
claim_re = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
class Claim:
    def __init__(self, line):
        match = claim_re.search(line)
        self.id =  int(match.group(1))
        self.x = int(match.group(2))
        self.y = int(match.group(3))
        self.w = int(match.group(4))
        self.h = int(match.group(5))
    def coords(self):
        return rectangle_coords(self.x, self.y, self.w, self.h)

class Puzzle:
    def __init__(self, lines):
        self.claims = []
        for line in lines:
            self.claims.append(Claim(line))
        
        self.grid = InfiniteGrid()

    def part1(self):
        for claim in self.claims:
            for coord in claim.coords():
                self.grid[coord] = self.grid[coord] + 1

        result = len(list(filter(lambda x: x > 1, self.grid.map.values())))   
        return result
        
    def part2(self):
        for claim in self.claims:
            found = True
            for coord in claim.coords():
            
                if self.grid[coord] > 1:
                    found = False
                    break
            if found:
                return claim.id

def parse_input(lines):
    return Puzzle(lines)    

def part1(puzzle):    
    
    return puzzle.part1()

def part2(puzzle):
    return puzzle.part2()
    