## advent of code 2021
## https://adventofcode.com/2021
## day 11

from aocpuzzle import *
from PrettyMap2D import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.reset()

    def reset(self):
        self.octopuses = Map2D()
        y = 0
        for line in self.lines:
            x = 0
            for c in line:
                self.octopuses[Coord2D(x, y)] = int(c)
                x += 1
            y += 1

    def increment(self, octs, coord):
        if coord not in octs:
            return False
        if octs[coord] == "x":            
            return False
        new_value = octs[coord] + 1
        if new_value == 10:
            octs[coord] = "x"
            return True
        octs[coord] = new_value
        
        return False


    def step(self, octs):
        flash_count = 0
        flashed = set()        
        for coord in octs:
            if self.increment(octs, coord):
                flashed.add(coord)        
        while(len(flashed) > 0):            
            new_flashed = set()

            for f in flashed:
                #print(f, "flashed")
                flash_count += 1
                for s in f.surrounding_coords():
                    if self.increment(octs, s):
                        new_flashed.add(s)     
            flashed = new_flashed       
        for coord in octs:
            if octs[coord] == "x":
                octs[coord] = 0        
        return flash_count

    def part1(self):
        #octs = self.octopuses.copy()
        flashes = 0
        for i in range(100):            
            flashes += self.step(self.octopuses)

        return flashes

    def part2(self):
        self.reset()
        step = 0
        while(True):
            step += 1
            flashes = self.step(self.octopuses)
            if flashes == len(self.octopuses):
                break
        return step