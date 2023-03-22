## advent of code 2019
## https://adventofcode.com/2019
## day 24

from aocpuzzle import *
from PrettyMap2D import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = Map2D()
        self.map.fill_from_lines(lines)
    
    def get_next_value(self, current, bug_count):
        if current == "#":
            if bug_count == 1:
                return "#"
            else:
                return "."
        else:
            if bug_count == 1 or bug_count == 2:
                return "#"
            else:
                return "."

    def tick(self, map):
        new_map = Map2D()
        for c in map:
            bug_count = 0
            for n in c.neighbors():
                if map[n] == "#":
                    bug_count += 1
            new_map[c] = self.get_next_value(map[c], bug_count)            
        return new_map
    
    def calculate_biodiversity(self, map):
        biodiversity = 0
        for c in map:
            if map[c] == "#":
                biodiversity += 2 ** (c.y * map.get_width() + c.x)        
        return biodiversity
    
    def part1(self):
        history = set()
        map = self.map
        time = 0
        
        while (True):
            #print(time)
            #map.print()
            #print()
            if map.__hash__() in history:
                map.print()
                print(time)
                return self.calculate_biodiversity(map)
            history.add(map.__hash__())
            map = self.tick(map)        
            time += 1           
            
    def neighbors(self, location):
        (layer, coord) = location
        n = coord + UP
        for d in NEIGHBORS:
            n = coord + d
            if n.x < 0:
                yield (layer - 1, Coord2D(1,2))
            elif n.x > 4:
                yield (layer - 1, Coord2D(3,2))
            elif n.y < 0:
                yield (layer - 1, Coord2D(2,1))
            elif n.y > 4:
                yield (layer - 1, Coord2D(2,3))
            elif n == Coord2D(2,2):
                if d == UP:
                    for x in range(5):
                        yield (layer + 1, Coord2D(x, 4))
                elif d == DOWN:
                    for x in range(5):
                        yield (layer + 1, Coord2D(x, 0))
                elif d == LEFT:
                    for y in range(5):
                        yield (layer + 1, Coord2D(4, y))
                elif d == RIGHT:
                    for y in range(5):
                        yield (layer + 1, Coord2D(0, y))
            else:
                yield (layer, n)


    def count_neighbor_bugs(self, map, location):

        count = 0
        for n in self.neighbors(location):
            if n in map:
                assert(map[n]) == "#"            
                count += 1
        #print(location, count)
        return count
    
    def should_be_bug(self, map, location):
        nbugs = self.count_neighbor_bugs(map, location)
        current = "."
        if (location in map):
            current = "#"
        if self.get_next_value(current, nbugs) == "#":
            return True
        return False
    
    def tick2(self, map):
        points = set()
        for c in map:
            points.add(c)
            for n in self.neighbors(c):
                points.add(n)

        new_map = {}
        for p in points:
            #print(p)
            if self.should_be_bug(map, p):
                new_map[p] = "#"
        return new_map

    def print_map(self, map):
        keys = map.keys()
        layers = list(set([k[0] for k in keys]))
        layers.sort()
        for layer in layers:
            print("Layer", layer)
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        print("?", end="")
                    elif (layer, Coord2D(x,y)) in map:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            print()

    def part2(self):
        
        map = {}
        for coord in self.map:
            if coord == Coord2D(2,2):
                continue
            if self.map[coord] == "#":
                map[(0,coord)] = self.map[coord]
        #self.print_map(map)
        if self.is_test:
            count = 10
        else:
            count = 200
        for i in range(count):
            #print(i, len(map))
            #self.print_map(map)
            map = self.tick2(map)
        #self.print_map(map)

        return len(map)