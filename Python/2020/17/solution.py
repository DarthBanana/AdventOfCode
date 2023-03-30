## advent of code 2020
## https://adventofcode.com/2020
## day 17

from aocpuzzle import *
from Map2D import *
from CoordND import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.graph = Map2D(lines = lines)       
        

    def tick(self):        
        new_map = set()
        coords_to_check = set()
        for coord in self.map:            
            for adj in coord.surrounding_coords():                
                coords_to_check.add(adj)

        for coord in coords_to_check:
            active_neighbors = 0
            for adj in coord.surrounding_coords():
                if adj in self.map:
                    active_neighbors += 1

            if coord in self.map:
                if active_neighbors == 2 or active_neighbors == 3:
                    
                    new_map.add(coord)
            else:
                if active_neighbors == 3:                   
                    new_map.add(coord)
        self.map = new_map

    def part1(self):
        self.map = set()
        for coord in self.graph:
            if self.graph[coord] == '#':                
                self.map.add(CoordND((coord.x, coord.y, 0)))
        
        for i in range(6):            
            self.tick()
            
        return len(self.map)

    def part2(self):
        self.map = set()
        for coord in self.graph:
            if self.graph[coord] == '#':                
                self.map.add(CoordND((coord.x, coord.y, 0, 0)))
        
        for i in range(6):            
            self.tick()
            
        return len(self.map)        
        