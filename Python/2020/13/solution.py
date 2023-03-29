## advent of code 2020
## https://adventofcode.com/2020
## day 13

from aocpuzzle import *
from parsehelp import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.earliest_departure = int(lines[0])
        self.buses = get_all_ints(lines[1])
        split = lines[1].split(",")
        t = 0
        self.bi = []
        self.ni = []
        for v in split:
            if v != "x":
                self.bi.append((int(v) - t%int(v))%int(v))
                self.ni.append(int(v))                
            t += 1


    def part1(self):
        times = []
        for b in self.buses:
            if self.earliest_departure % b == 0:
                return 0
            else:
                times.append((b, b * (self.earliest_departure // b + 1) - self.earliest_departure))
        times.sort(key=lambda x: x[1])
        return times[0][0] * times[0][1]

    def part2(self):
        # https://en.wikipedia.org/wiki/Chinese_remainder_theorem

        N = 1
        for n in self.ni:
            N *= n
            
        Ni = [N//n for n in self.ni]
        xi = []
        product = []

        for i in range(len(self.ni)):            
            x  = 1
            while (Ni[i]*x)%self.ni[i] != 1:
                x += 1
            xi.append(x)
            product.append(xi[i]*Ni[i]*self.bi[i])
        return sum(product)%N


