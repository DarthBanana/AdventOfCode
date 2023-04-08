## advent of code 2021
## https://adventofcode.com/2021
## day 05

from aocpuzzle import *
from parsehelp import *
from Map2D import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)        
        self.line_segments = []
        self.map = Map2D()
        for line in lines:
            nums = get_all_ints(line)
            self.line_segments.append((Coord2D(nums[0],nums[1]),Coord2D(nums[2],nums[3])))

    def part1(self):
        
        for start,end in self.line_segments:
            if start.x == end.x or start.y == end.y:                            
                for coord in CoordsInLineHV45(start, end):                
                    self.map[coord] = self.map.get(coord, 0) + 1
        count = 0
        for v in self.map.values():
            if v >= 2:
                count += 1
        return count

    def part2(self):
        self.map = Map2D()
        for start,end in self.line_segments:
            for coord in CoordsInLineHV45(start, end):                
                self.map[coord] = self.map.get(coord, 0) + 1
        count = 0
        for v in self.map.values():
            if v >= 2:
                count += 1
        return count
