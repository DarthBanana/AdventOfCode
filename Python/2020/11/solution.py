## advent of code 2020
## https://adventofcode.com/2020
## day 11

from time import sleep
from aocpuzzle import *
from PrettyMap2D import *
HALF_DIRECTIONS = [E, SE, S, SW]
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)        
        self.visible = {} 

    def next_map(self, map):                
        changes = []
        for coord in map:            
            #print(coord)
            if map[coord] == "L":
                if map.count_surrounding(coord, "#") == 0:
                    #print("changing to #")
                    changes.append((coord, "#"))                    
            elif map[coord] == "#":
                if map.count_surrounding(coord, "#") >= 4:
                    
                    #print("changing to L")
                    changes.append((coord, "L"))
        changed = False
        for c, v in changes:
            changed = True
            map[c] = v
        return changed
    
    def next_map2(self, map):

        changes = []
        for coord, visible in self.visible.items(): 
            count = 0
            for c in visible:
                if map[c] == "#":
                    count += 1
            
            if map[coord] == "L":
                if count == 0:
                    #print("changing to #")
                    changes.append((coord, "#"))                    
            elif map[coord] == "#":
                if count > 4:
                    
                    #print("changing to L")
                    changes.append((coord, "L"))
        changed = False
        for c, v in changes:
            changed = True
            map[c] = v
        return changed
    
    def count_seen(self, map, coord):
        count = 0
        visible = self.visible[coord]
        for c in visible:
            if map[c] == "#":
                count += 1
        return count

    

    def find_visible(self, map):
        for c in map:
            if map[c] == ".":
                continue
            if c not in self.visible:
                visible = []
            else:
                visible = self.visible[c]
            
            for d in HALF_DIRECTIONS:
                c2 = c
                while True:
                    c2 = c2 + d
                    if not c2 in map:
                        break
                    if map[c2] == "#" or map[c2] == "L":
                        visible.append(c2)
                        if c2 not in self.visible:
                            self.visible[c2] = []
                        self.visible[c2].append(c)
                        break
            self.visible[c] = visible
            
    def part1(self):
        map = Map2D(lines=self.lines)        
        count = 0
        while self.next_map(map):
            print("1", count)
            count += 1
            pass
        return map.count("#")

    def part2(self):
        map = Map2D(lines=self.lines)      
        self.find_visible(map)  
        count = 0
        print("2", count)
        while self.next_map2(map):
            count += 1
            print("2", count)
            
            pass
        return map.count("#")