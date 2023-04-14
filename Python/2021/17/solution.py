## advent of code 2021
## https://adventofcode.com/2021
## day 17

from aocpuzzle import *
from parsehelp import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        ints = get_all_ints(lines[0])
        self.target_minx = ints[0]
        self.target_maxx = ints[1]
        self.target_miny = ints[2]
        self.target_maxy = ints[3]

    def test_x(self, v):
        x = 0
        t = 0
        times = set()
        while x <= self.target_maxx:
            if x >= self.target_minx:
                times.add(t)
            if v == 0:
                if x >= self.target_minx:
                    # stopped in target so 
                    # all times greater than the max
                    # are also valid.  Add 0 to denote this
                    times.add(0)
                break                
            x += v
            t += 1
            v -= 1
        return times
    def test_y2(self, v):
        y = 0
        t = 0
        times = set()
        while y >= self.target_miny:
            if y <= self.target_maxy:
                times.add(t)
            y += v
            t += 1
            v -= 1
        return times

    def test_y(self, v):
        #print("Testing ", v)
        y = 0
        max_y = 0
        while(y > self.target_maxy):
            y += v
            #print(y)
            max_y = max(max_y, y)
            v -= 1
        if y >= self.target_miny:
            #print("HIT")
            return True, max_y
        #print("MISS")
        return False, max_y
    def part1(self):
        max_y = 0
        y = 0
        for y in range(1, abs(self.target_miny) + 1):
            result, my = self.test_y(y)
            if result:                
                max_y = max(max_y, my)
            print(y, my, result)            
         
        return max_y
    def part2(self):
        x_ranges = {}
        x_candidates = set()
        y_ranges = {}
        y_candidates = set()
        for x in range(1, self.target_maxx + 1):
            times = self.test_x(x)
            if len(times) > 0:
                x_ranges[x] = times
                x_candidates.add(x)
            
        for y in range(self.target_miny, abs(self.target_miny)+1):
            times = self.test_y2(y)
            if len(times) > 0:
                y_ranges[y] = times
                y_candidates.add(y)
        candidates = set()
        for y in y_candidates:
            y_times = y_ranges[y]
            for x in x_candidates:
                x_times = x_ranges[x]
                if len(x_times & y_times) > 0:
                    candidates.add((x,y))
                elif 0 in x_times:
                    # stopped in target
                    max_xt = max(x_times)
                    for t in y_times:
                        if t > max_xt:
                            candidates.add((x,y))
                            break
        can = list(candidates)

        return len(candidates)


        