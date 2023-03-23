## advent of code 2019
## https://adventofcode.com/2019
## day 01
from aocpuzzle import *
from parsehelp import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)        
        self.masses =  get_int_per_line(lines)   

    def calculate_fuel(self, mass):
        return (mass // 3) - 2
    
    def calculate_fuel2(self, mass):
        fuel = self.calculate_fuel(mass)
        if fuel <= 0:
            return 0
        return fuel + self.calculate_fuel2(fuel)
    
    def part1(self):
        total = 0
        for mass in self.masses:
            total += self.calculate_fuel(mass)
        return total

    def part2(self):
        total = 0
        for mass in self.masses:
            total += self.calculate_fuel2(mass)
        return total