## advent of code 2019
## https://adventofcode.com/2019
## day 10

from collections import deque
import math
from aocpuzzle import *
from Map2D import *
import networkx as nx
from bresenham import bresenham
import matplotlib.pyplot as plt

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.map = InfiniteGrid()
        self.map.fill_from_lines(lines)
        self.asteroids = []
        self.station = None
        for coord in self.map:
            if self.map[coord] == '#':
                self.asteroids.append(coord)
            elif self.map[coord] == '.':
                pass
            else:
                assert(False)        
    def angle1(self, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        result = (math.atan2(dy, dx) * 180 / math.pi) + 90
        result += 720
        result %= 360
        if result < 0:
            result += 360
        assert(result >= 0 and result < 360)
        return result
    
    def angle2(self, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dx_reduced = dx // math.gcd(dx, dy)
        dy_reduced = dy // math.gcd(dx, dy)
        return (dx_reduced, dy_reduced)
    
    def build_angles_for_node(self, node, asteroids):
        angles = {}
        asteroids.sort(key=lambda c: c.distance(node))
        for a in asteroids:
            if a == node:
                continue
            
            angle = self.angle1(node, a)
            if angle not in angles:
                angles[angle] = deque([a])
            else:
                angles[angle].append(a)
        return angles
    
    def sweep(self, angles, destroyed):        
        sorted_angles = list(angles.keys())
        sorted_angles.sort()               
        asteroid = None

        for angle in sorted_angles:
            assert(len(angles[angle]) > 0)
            asteroid = angles[angle].popleft()
            destroyed.append(asteroid)
            if len(angles[angle]) == 0:
                del angles[angle]
           
        return destroyed

    def pew(self, asteroids, station, count):
        angles = self.build_angles_for_node(station, asteroids.copy())
    
        destroyed = []

        while len(destroyed) < count and len(angles) > 0:

            destroyed = self.sweep(angles, destroyed)
            
        return destroyed


    def part1(self):
        asteroids = self.asteroids.copy()
        max_asteroids = 0
        max_asteroid = None

        for a in asteroids:
            angles = self.build_angles_for_node(a, asteroids.copy())
            num_asteroids = len(angles)
            if num_asteroids > max_asteroids:
                max_asteroids = num_asteroids
                max_asteroid = a
        print(max_asteroid, max_asteroids)
        self.station = max_asteroid
        if self.is_test:
            return (max_asteroid, max_asteroids)
        
        return max_asteroids    
        

    def part2(self):
        if self.is_test:
            counts = [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]
            target = 300
        else:
            counts = [200]
            target = 201
            #for count in counts: 
        print("UP ANGLE: ",self.angle1(self.station, self.station + UP))       
        print("RIGHT ANGLE: ",self.angle1(self.station, self.station + RIGHT))
        print("DOWN ANGLE: ",self.angle1(self.station, self.station + DOWN))
        print("LEFT ANGLE: ",self.angle1(self.station, self.station + LEFT))
        destroyed = self.pew(self.asteroids.copy(), self.station, target)
        results = []
        for c in counts:
            if c <= len(destroyed):
                results.append((c,destroyed[c - 1]))
        #print(destroyed)
        if self.is_test:
            return results
        return destroyed[199].x * 100 + destroyed[199].y

        
        