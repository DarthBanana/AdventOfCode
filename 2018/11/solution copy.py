## advent of code 2018
## https://adventofcode.com/2018
## day 11
from Map2D import *

class Puzzle:
    def __init__(self, lines):
        self.sn = int(lines[0])
        self.grid = [0 for _ in range(301)InfiniteGrid()
        self.partial_sums = InfiniteGrid()
        
    def get_cell_value(self, coord):
        rackID = coord.x + 10
        pl = rackID * coord.y
        pl += self.sn
        pl *= rackID
        pl = pl // 10**2
        pl %= 10
        pl -= 5
        return pl

    def calc_partial_sum(self, coord):
        return self.grid[coord] + self.partial_sums[coord + W] + self.partial_sums[coord + N] - self.partial_sums[coord + NW]

    def build_grid(self):        
        for coord in rectangle_coords(1, 1, 300, 300):
            self.grid[coord] = self.get_cell_value(coord)

    def build_partial_sums(self):
        for coord in rectangle_coords(2,2,299, 299):
            self.partial_sums[coord] = self.calc_partial_sum(coord)


    def part1(self):
        self.build_grid()
        scores = []
        for coord in rectangle_coords(2, 2, 298, 298):
            score = self.grid[coord] #self.get_cell_value(coord)
            for other in coord.surrounding_coords():
                score += self.grid[other] #self.get_cell_value(other)
            scores.append((score, coord))

        scores.sort(key=lambda k:k[0])
        score, coord = scores.pop()
        result = coord + NW
        return "{},{}".format(result.x, result.y)

    def get_rect_score(self, coord, dim):
        score = 0
        for c in coord.rectangle_tl_coords(dim, dim):
            score += self.grid[c]
        return score

    def part2(self):
        result = (0, (0,0, 0))
        grid_sums = {}
        self.build_partial_sums()
        for size in range(1,301):
            print(size)
            for coord in rectangle_coords(1, 1, 300-size, 300-size):
                gp = self.partial_sums[coord + size * SE] - self.partial_sums[coord + size * S] -self.partial_sums[coord + size * E] + self.partial_sums[coord]
                result = max(result, (gp, (coord.x, coord.y, size)))
        print(result)
        #coord, size =  grid_sums[max(grid_sums)]

        return "{},{},{}".format(resultcoord.x, coord.y, size)
        return grid_sums
        scores = []        
        for dim in range(3,301):
            print(dim)
            for coord in rectangle_coords(1, 1,300-dim, 300-dim):
                score = self.get_rect_score(coord, dim)
                scores.append((score, coord, dim))
        scores.sort(key=lambda k:k[0])
        score, coord, dim = scores.pop()
        return "{},{},{}".format(coord.x, coord.y, dim)

        