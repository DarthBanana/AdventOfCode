## advent of code 2018
## https://adventofcode.com/2018
## day 23

import re
from CoordND import *
from z3 import *
def zabs(x):
  return If(x >= 0,x,-x)
def man_dist(x,y):
    return zabs(x[0]-y[0]) + zabs(x[1]-y[1]) + zabs(x[2]-y[2])
line_re = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
class Puzzle:
    def __init__(self, lines):
        self.nanobots = []
        for line in lines:
            m = line_re.match(line)
            self.nanobots.append((CoordND((int(m.group(1)), int(m.group(2)), int(m.group(3)))), int(m.group(4))))
        self.nanobots.sort(key=lambda x: x[0])
        
    def nanobots_in_range(self, coord):
        return sum(1 for nanobot in self.nanobots if nanobot[0].manhattan_dist(coord) <= nanobot[1])
    def part1(self):    
        strongest = max(self.nanobots, key=lambda x: x[1])
        return sum(1 for nanobot in self.nanobots if nanobot[0].manhattan_dist(strongest[0]) <= strongest[1])

    def part2(self):
        s = Solver()
        o = Optimize()
        (x, y, z) = (Int('x'), Int('y'), Int('z'))
        in_ranges = [Int('in_range_' + str(i)) for i in range(len(self.nanobots))]
        range_count = Int('sum')
        for i in range(len(self.nanobots)):
            in_ranges[i] = If(man_dist(self.nanobots[i][0].as_tuple(),(x,y,z)) <= self.nanobots[i][1], 1, 0)
        o.add(range_count == sum(in_ranges))
        dist_from_zero = Int('dist')
        o.add(dist_from_zero == man_dist((x,y,z), (0,0,0)))
        h1 = o.maximize(range_count)
        h2 = o.minimize(dist_from_zero)
        
        o.check()
        return(o.lower(h2))
        

        