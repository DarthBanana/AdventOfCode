## advent of code 2019
## https://adventofcode.com/2019
## day 12

import copy
from functools import reduce
from math import lcm
import math
from aocpuzzle import *
from parsehelp import *
from CoordND import *
class Moon:
    def __init__(self, pos):
        self.pos = CoordND(pos)
        self.vel = CoordND((0,0,0))
    def update_velocity(self, other):
        for i in range(3):
            if self.pos[i] < other.pos[i]:
                self.vel[i] += 1                
            elif self.pos[i] > other.pos[i]:
                self.vel[i] -= 1
                
    def potential_energy(self):
        return self.pos.dist()
    def kinetic_energy(self):
        return self.vel.dist()
    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()
        
    def __str__(self):
        return f"pos={self.pos}, vel={self.vel}"
    def __repr__(self):
        return f"pos={self.pos}, vel={self.vel}"
    def __hash__(self):
        return hash((self.pos, self.vel))
    
    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel


def _lcm(a, b):
    return (a * b) // math.gcd(a, b)


def lcm(lst):
    return reduce(_lcm, lst)

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.original_moons = []
        if is_test:
            self.iterations = int(lines[0])
            lines = lines[1:]
        else:
            self.iterations = 1000
        for line in lines:
            vals = get_all_ints(line)
            self.original_moons.append(Moon(vals))
        self.reset()

    def reset(self):
        self.moons = copy.deepcopy(self.original_moons)
    
    def update_velocities(self):
        for i in range(len(self.moons)):
            for j in range(i+1, len(self.moons)):
                moon1 = self.moons[i]
                moon2 = self.moons[j]
                moon1.update_velocity(moon2)
                moon2.update_velocity(moon1)
                
    def update_positions(self):
        for moon in self.moons:
            moon.pos += moon.vel

    def total_energy(self):
        return sum(moon.total_energy() for moon in self.moons)
    
    def part1(self):
        for i in range(self.iterations):
            self.update_velocities()
            self.update_positions()        
        return self.total_energy()
    def build_hash(self):
        return hash(frozenset(self.moons))
        
    def is_dim_start_state(self, dim):
        for i in range(len(self.moons)):
            if self.moons[i].vel[dim] != 0:
                return False
            if self.moons[i].pos[dim] != self.original_moons[i].pos[dim]:
                return False
        return True
    
    def part2(self):
        self.reset()
        dimension_cycles = [None, None, None]

        count = 0
        while True:
            self.update_velocities()
            self.update_positions()
            count += 1
            for i in range(3):
                if dimension_cycles[i] is None:
                    if self.is_dim_start_state(i):
                        print(f"state repeat for dimension {i}: {count}")
                        dimension_cycles[i] = count
            if all(dimension_cycles):
                break
        print(dimension_cycles)
        return lcm(dimension_cycles)
    
        