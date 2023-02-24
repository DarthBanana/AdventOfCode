## advent of code 2018
## https://adventofcode.com/2018
## day 18
import copy
import json
from Map2D import *
class Puzzle:
    def __init__(self, lines):
        self.original_map = InfiniteGrid(".")
        self.original_map.fill_from_lines(lines)        
        
    def get_next_state(self, map, coord):
        trees = 0
        lumberyards = 0
        for adj in coord.surrounding_coords():
            acre = map[adj]
            if acre == "|":
                trees += 1
            elif acre == "#":
                lumberyards += 1
        acre = map[coord]
        if acre == ".":
            if trees >= 3:
                return "|"
            return "."
        elif acre == "|":
            if lumberyards >= 3:
                return "#"
            return "|"
        elif acre == "#":
            if lumberyards >= 1 and trees >= 1:
                return "#"
            return "."
        else:
            assert(False)

    def get_next_map(self, map):
        new_map = InfiniteGrid(".")
        for coord in map.rectangle_coords():
            new_map[coord] = self.get_next_state(map, coord)
        return new_map

    def run_minutes(self, map, minutes):
        for i in range(minutes):
            map = self.get_next_map(map)
        return map

    def count_em(self, map):
        trees = 0
        lumberyards = 0
        for coord in map.rectangle_coords():
            if map[coord] == "|":
                trees += 1
            elif map[coord] == "#":
                lumberyards += 1
        return trees, lumberyards

    def part1(self):
        map = copy.deepcopy(self.original_map)
        map = self.run_minutes(map, 10)
        trees, lumberyards = self.count_em(map)
        return trees * lumberyards

    def part2(self):
        history = {}
        time = 0
        map = copy.deepcopy(self.original_map)
        target_time = 1000000000
        found_cycle = False
        while time < target_time:
            #map.print()
            #print(hash(map))
            if not found_cycle:
                if hash(map) in history:
                    # found a cycle
                    print("Found cycle at time ", time)
                    time_seen = history[hash(map)]
                    cycle_len = time - time_seen
                    time_left = target_time - time
                    remainder = time_left % cycle_len
                    time = target_time - remainder
                    
                    found_cycle = True
                else:
                    history[hash(map)] = time
            map = self.get_next_map(map)
        
            time += 1
        trees, lumberyards = self.count_em(map)
        return trees * lumberyards
            