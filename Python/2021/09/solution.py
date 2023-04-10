## advent of code 2021
## https://adventofcode.com/2021
## day 09

from aocpuzzle import *
from Map2D import *
from mapgraph import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = Map2D()
        
        y = 0        
        for line in lines:
            x = 0
            for c in line:
                self.map[Coord2D(x,y)] = int(c)
                x += 1
            y += 1
        self.graph = generate_neighbor_graph_from_map(self.map, [0,1,2,3,4,5,6,7,8])

    def is_low_point(self, coord):
        v = self.map[coord]
        for n in coord.neighbors():
            if n in self.map:
                if self.map[n] <= v:
                    return False
        return True

    def part1(self):
        total = 0
        for coord in self.map:
            if self.is_low_point(coord):
                total += self.map[coord] + 1
        return total

    def part2(self):
        total = 1
        basins = [len(c) for c in nx.connected_components(self.graph)]
        basins.sort(reverse=True)
        
        for i in range(3):
            total *= basins[i]
        return total


        pass