## advent of code 2021
## https://adventofcode.com/2021
## day 07

from aocpuzzle import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.crab_positions = get_all_ints(lines[0])
        self.build_nonconstant_fuel_table()
        
    def build_nonconstant_fuel_table(self):
        self.nonconstant_fuel_table = {}
        for i in range((max(self.crab_positions)-min(self.crab_positions)) + 1):
            self.nonconstant_fuel_table[i] = self.calculate_nonconstant_fuel(i)

    def calculate_nonconstant_fuel(self, dist):
        
        fuel = 0
        for i in range(1, dist+1):
            fuel+= i        
        return fuel

    def calculate_fuel(self, position, nonconstant = False):
        if nonconstant:
            return sum([self.nonconstant_fuel_table[abs(p-position)] for p in self.crab_positions])
        return sum([abs(p-position) for p in self.crab_positions])
    
    def find_min_fuel(self, nonconstant = False):
        min_fuel = 1000000000
        for i in range(min(self.crab_positions), max(self.crab_positions)):                  
            min_fuel = min(min_fuel, self.calculate_fuel(i, nonconstant))
        return min_fuel
    
    def part1(self):
        return self.find_min_fuel()

    def part2(self):
        return self.find_min_fuel(True)
        pass