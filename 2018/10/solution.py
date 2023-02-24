## advent of code 2018
## https://adventofcode.com/2018
## day 10

from msvcrt import getch
import os
import re
import time
from Map2D import *

puzzle_re = re.compile(r"position=\<\s*(-?\d+),\s*(-?\d+)\> velocity=<\s*(-?\d+),\s*(-?\d+)\>")
class Puzzle:
    def __init__(self, lines):
        self.time = 0
        self.points = []
        for line in lines:
            match = puzzle_re.search(line)
            self.points.append((Coord2D(int(match.group(1)), int(match.group(2))), Coord2D(int(match.group(3)), int(match.group(4)))))

    def get_points_at_time(self, time):
        points = []
        for p, v in self.points:
            points.append(p + v*time)
        points.sort(key=lambda p: p.x)
        width = (points[-1].x + 1) - points[0].x
        return points, width
    
    def draw_points(self, points):
        grid = InfiniteGrid('.')
        for p in points:
            grid[p] = "#"
        grid.print()

    def part1(self):
        
        self.time = 0
        prev_width = sys.maxsize
        min_width = sys.maxsize
        roll_back_point = 0
        min_time = 0
        step_size = 10000
        print(self.time)
        while True:
            points, width = self.get_points_at_time(self.time)
            if width < prev_width:                
                min_time = self.time
                min_width = width                
            elif width > prev_width:                
                if abs(step_size) == 1:
                    self.time = min_time
                    break                
                step_size = -1*step_size // 10                
                
            prev_width = width
            self.time += step_size
        
            
        while(True):
            os.system('CLS')
            print("Time:",self.time)
            points, width = self.get_points_at_time(self.time)
            self.draw_points(points)
            answer = input ("Enter message : ")
            return answer            

    def part2(self):
        return self.time
        