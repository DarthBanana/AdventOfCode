## advent of code 2020
## https://adventofcode.com/2020
## day 24

from time import sleep
from aocpuzzle import *

HEX_ADJACENT = [(2,0), (1,1), (-1,1), (-2,0), (-1,-1), (1,-1)]
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        
        self.always_run_part_1 = True

        self.black_tiles = set()
        self.neighbors = {}


    def find_tile(self, path):
        i = 0
        cur = (0,0)
        while i < len(path):
            d = path[i]
            i += 1

            if d == "e":
                cur = (cur[0] + 2, cur[1])
            elif d == "w":
                cur = (cur[0] - 2, cur[1])
            else:            
                od = path[i]
                i += 1
                delta_y = 0
                delta_x = 0
                if d == "n":
                    delta_y = -1
                else:
                    assert(d == "s")
                    delta_y = 1
                if od == "e":
                    delta_x = 1
                else:
                    assert(od == "w")
                    delta_x = -1
                cur = (cur[0] + delta_x, cur[1] + delta_y)
        return cur
    
    def flip_tile(self, coord):
        
        if coord in self.black_tiles:
            self.black_tiles.remove(coord)
        else:
            self.black_tiles.add(coord)
    
    def get_neighbors(self, coord):
        if coord in self.neighbors:
            return self.neighbors[coord]

        neighbors = set()
        for a in HEX_ADJACENT:
            neighbors.add((coord[0] + a[0], coord[1] + a[1]))
        self.neighbors[coord] = neighbors
        return neighbors

    def get_tiles_to_check(self):
        tiles = set()

        for coord in self.black_tiles:
            tiles.add(coord)            
            tiles.update(self.get_neighbors(coord))
        return tiles
    

    def get_black_neighbor_count(self, coord):

        neighbors = self.get_neighbors(coord)
        count = len(self.black_tiles & neighbors)
        return count


    def tick(self):
        new_tiles = set()
        coords_to_check = self.get_tiles_to_check()
        for coord in coords_to_check:
            count = self.get_black_neighbor_count(coord)
            if coord in self.black_tiles:
                if count == 0 or count > 2:
                    pass
                else:
                    new_tiles.add(coord)
            else:
                if count == 2:
                    new_tiles.add(coord)
        self.black_tiles = new_tiles

    def part1(self):
        for line in self.lines:
            coord = self.find_tile(line)
            self.flip_tile(coord)
        return len(self.black_tiles)
        

    def part2(self):
        for i in range(100):
            #print(i)
            self.tick()            
        return len(self.black_tiles)        