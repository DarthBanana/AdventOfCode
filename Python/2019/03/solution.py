## advent of code 2019
## https://adventofcode.com/2019
## day 03
from PrettyMap2D import *
from aocpuzzle import *
class Move:
    def __init__(self, instruction):
        d = instruction[0]
        self.dist = int(instruction[1:])
        if d == 'R':
            self.direction = RIGHT
        elif d == 'L':
            self.direction = LEFT
        elif d == 'U':
            self.direction = UP
        elif d == 'D':
            self.direction = DOWN


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.wires = []
        for line in lines:
            moves = []
            directions = line.split(',')
            for d in directions:
                moves.append(Move(d))
            self.wires.append(moves)
        self.red_map = Map2D('.')
        self.blue_map = self.red_map.add_overlay(1)        
        self.red_steps = {}
        self.blue_steps = {}
        self.intersections = []

    def part1(self):
        print("RED_WIRE")
        red_wire = self.wires[0]        
        cur = Coord2D(0,0)
        steps = 0
        for m in red_wire:
            for d in range(m.dist):
                steps += 1                
                cur += m.direction                                
                self.red_map[cur] = 'R'                
                if not cur in self.red_steps:
                    self.red_steps[cur.copy()] = steps        
        print("BLUE_WIRE")
        blue_wire = self.wires[1]
        steps = 0
        cur = Coord2D(0,0)
        for m in blue_wire:
            for d in range(m.dist):
                cur = cur + m.direction
                steps += 1
                if self.red_map[cur] == 'R':
                    self.intersections.append(cur)
                self.blue_map[cur] = 'B'
                if not cur in self.blue_steps:
                    self.blue_steps[cur] = steps
        #self.red_map.print()
        assert(len(self.intersections) > 0)
        
        return min([x.distance(Coord2D(0,0)) for x in self.intersections ])
             

    def part2(self):
        assert(len(self.intersections) > 0)
        distances = []
        for i in self.intersections:
            print(i, ": red dist =",self.red_steps[i], ", blue dist =", self.blue_steps[i])
            distances.append(self.red_steps[i] + self.blue_steps[i])

        return min(distances)