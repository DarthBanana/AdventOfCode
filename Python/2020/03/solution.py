## advent of code 2020
## https://adventofcode.com/2020
## day 03

from time import sleep
from aocpuzzle import *
from PrettyMap2D import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = Map2D()
        self.map.fill_from_lines(lines)
        self.toboggan_layer = self.map.add_overlay(1)
        
        self.original_width = self.map.maxx + 1
            
    def add_another_copy(self):
        offset = Coord2D(self.map.maxx+1,0)
        for c in rectangle_coords(0, 0, self.original_width, self.map.get_height()):
            self.map[c+offset] = self.map[c]

    def count_trees(self, slope):
        current_pos = Coord2D(0, 0)
        trees = 0
        self.toboggan_layer[current_pos] = "O"
        while(current_pos.y <= self.map.maxy):
            current_pos = current_pos + slope
            current_pos.x = current_pos.x % self.map.get_width()

            if self.map[current_pos] == "#":
                self.toboggan_layer[current_pos] = "X"
                trees += 1
            else:
                self.toboggan_layer[current_pos] = "O"                        
        return trees
    
    def part1c(self):
        return self.count_trees(Coord2D(3,1))
    
    def part1b(self):
        current_pos = Coord2D(0, 0)
        trees = 0
        self.toboggan_layer[current_pos] = "O"
        while(current_pos.y <= self.map.maxy):
            current_pos = current_pos + Coord2D(3, 1)
            current_pos.x = current_pos.x % self.map.get_width()

            if self.map[current_pos] == "#":
                self.toboggan_layer[current_pos] = "X"
                trees += 1
            else:
                self.toboggan_layer[current_pos] = "O"                        
        return trees
    
    def part1a(self):
        current_pos = Coord2D(0, 0)
        trees = 0
        self.toboggan_layer[current_pos] = "O"
        while(current_pos.y <= self.map.maxy):
            current_pos = current_pos + Coord2D(3, 1)
            if current_pos.x > self.map.maxx:
                self.add_another_copy()
            if self.map[current_pos] == "#":
                self.toboggan_layer[current_pos] = "X"
                trees += 1
            else:
                self.toboggan_layer[current_pos] = "O"                        
        return trees
    
    def part1(self):
        return self.part1c()

    def part2(self):
        slopes = [Coord2D(1,1), Coord2D(3,1), Coord2D(5,1), Coord2D(7,1), Coord2D(1,2)]
        total = 1
        for slope in slopes:
            total *= self.count_trees(slope)
        return total
        