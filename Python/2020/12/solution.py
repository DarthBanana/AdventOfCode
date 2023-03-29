## advent of code 2020
## https://adventofcode.com/2020
## day 12

from aocpuzzle import *
from PrettyMap2D import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.instructions = []
        for line in lines:
            self.instructions.append((line[0], int(line[1:])))
        self.reset()

    def reset(self):
        self.pos = Coord2D(0, 0)
        self.dir = E
        self.waypoint = Coord2D(10, -1)

    def rotate_waypoint(self, degrees):
        if degrees % 90 != 0:
            raise Exception("Can only rotate in 90 degree increments")
        steps = degrees // 90
        for i in range(steps):
            self.waypoint = Coord2D(self.waypoint.y, -self.waypoint.x)

    def act(self, action, value):
        if action == 'N':
            self.pos = self.pos + (N * value)
        elif action == 'S':
            self.pos = self.pos + (S * value)
        elif action == 'E':
            self.pos = self.pos + (E * value)
        elif action == 'W':
            self.pos = self.pos + (W * value)
        elif action == 'L':            
            self.dir = turn(self.dir, -value)            
        elif action == 'R':            
            self.dir = turn(self.dir, value)            
        elif action == 'F':
            self.pos = self.pos + (self.dir * value)

    def part1(self):
        for i in self.instructions:
            self.act(i[0], i[1])
        return self.pos.manhattan_distance(Coord2D(0, 0))
    
    def act2(self, action, value):
        if action == 'N':
            self.waypoint = self.waypoint + (N * value)
        elif action == 'S':
            self.waypoint = self.waypoint + (S * value)
        elif action == 'E':
            self.waypoint = self.waypoint + (E * value)
        elif action == 'W':
            self.waypoint = self.waypoint + (W * value)
        elif action == 'L':        
            self.rotate_waypoint(value)
            
        elif action == 'R':            
            self.rotate_waypoint(360-value)
            
        elif action == 'F':
            self.pos = self.pos + (self.waypoint * value)

    def part2(self):
        self.reset()
        for i in self.instructions:
            self.act2(i[0], i[1])
            
        return self.pos.manhattan_distance(Coord2D(0, 0))