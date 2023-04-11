## advent of code 2021
## https://adventofcode.com/2021
## day 13

from aocpuzzle import *
from PrettyMap2D import *
from parsehelp import *

fold_re = re.compile(r"fold along ([xy])=(\d+)")
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.reset()
        print(self.folds)

    def reset(self):
        self.folds = []
        self.coords = []
        for line in self.lines:
            if len(line) == 0:
                continue
            if line[0] == "f":
                match = fold_re.match(line)
                self.folds.append((match[1], int(match[2])))
            else:
                nums = get_all_ints(line)                
                self.coords.append(Coord2D(nums[0], nums[1]))
        
        self.map = Map2D(" ")
        for coord in self.coords:
            self.map[coord] = "#"

    def fold_y(self, offset):
        coords_to_move = []
        for coord in self.map:
            if coord.y > offset:
                coords_to_move.append(coord)
        for coord in coords_to_move:
            del self.map[coord]
            new_coord = coord
            new_coord.y = offset - (new_coord.y - offset)
            self.map[new_coord] = "#"

    def fold_x(self, offset):
        coords_to_move = []
        for coord in self.map:
            if coord.x > offset:
                coords_to_move.append(coord)
        for coord in coords_to_move:
            del self.map[coord]
            new_coord = coord
            new_coord.x = offset - (new_coord.x - offset)
            self.map[new_coord] = "#"
                    
    def fold(self, axis, offset):
        if axis == "y":
            return self.fold_y(offset)
        else:
            return self.fold_x(offset)

    def part1(self):
        a, o = self.folds[0]        
        self.fold(a, o)        
        return len(self.map)

        

    def part2(self):
        self.reset()
        for a, o in self.folds:
            self.fold(a,o)            
        self.map.reset_minmax()
        self.map.refresh()
        self.map.print()        
        return "EPUELPBR"