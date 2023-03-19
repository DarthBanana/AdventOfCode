# advent of code 2019
# https://adventofcode.com/2019
# day 18

from collections import deque
import copy
from Map2D import Map2D
from aocpuzzle import *
from mapgraph import *

def get_key_bit(key):
    return 1 << (ord(key) - ord("a"))
def get_door_bit(door):
    return 1 << (ord(door) - ord("A"))

def get_keys_from_set(keys):
    key_bits = 0
    for key in keys:
        key_bits |= get_key_bit(key)

    return key_bits


def get_pois_for_map(map):
        keys = set()
        doors = set()
        pois = {}
        
        for coord in map:
            value = map[coord]
            if value == "." or value == "#":
                continue
            pois[value] = coord
            if value in "abcdefghijklmnopqrstuvwxyz":
                keys.add(value)
            if value in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                doors.add(value)            
        return (pois, keys, doors)

def get_paths_from_point(point, pois, map):
    pos = pois[point]
    paths = {}

    dist = 0
    queue = deque()
    history = {}
    queue.append((pos, dist))
    while (len(queue)):
        (pos, dist) = queue.popleft()
        if pos in history:
            continue
        history[pos] = dist
        value = map[pos]
        if value != "." and value != point:
            paths[value] = dist
            continue
        for n in pos.neighbors():
            if (map[n] == None):
                print(pos, n)
                assert(False)
            if map[n] == "#":
                continue
            queue.append((n, dist+1))
    return paths



def build_reduced_graph(map, pois):
    reduced_graph = nx.Graph()
    for p in pois:
        paths = get_paths_from_point(p, pois, map)
        for d in paths:
            reduced_graph.add_edge(p, d, weight=paths[d])

    return reduced_graph

class SubMap:
    
    def __init__(self, map) -> None:
        self.map = map
        self.pois, self.keys, self.doors = get_pois_for_map(map)
        self.reduced_graph = build_reduced_graph(self.map, self.pois)



class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = Map2D()
        self.map.fill_from_lines(lines)
        self.map.print()
        self.points_of_interest = {}
        self.keys = set()
        self.doors = set()        
        self.graphs = {}        


    def get_pois(self):
        self.points_of_interest, self.keys, self.doors = get_pois_for_map(self.map)
        

    def bfs_b(self, reduced_graph):
        keys_left = self.keys
        history = {}
        queue = deque()
        print(reduced_graph)
        queue.append(("@", keys_left, 0, []))
        print(reduced_graph["@"])
        best_steps = 10000000000
        best_path = None
        while(len(queue)):
            (poi, keys_left, steps, path) = queue.popleft()
            
            if len(keys_left) == 0:  
                if steps < best_steps:
                    best_steps = steps
                    best_path = path
                continue

            keys_hash = list(keys_left)
            keys_hash.sort()
            keys_hash = tuple(keys_hash)
            
            if (poi, keys_hash) in history:
                if history[(poi, keys_hash)] <= steps:
                    continue
            history[(poi, keys_hash)] = steps
            
            for n in reduced_graph[poi]:                
                if n in self.doors:
                    if n.lower() in keys_left:
                        continue                                
                queue.append((n, keys_left - set(n), steps + reduced_graph[poi][n]["weight"], path + [n]))


        return (best_steps, best_path)
        


    def part1b(self):
        self.get_pois()
        reduced_graph = build_reduced_graph(self.map, self.points_of_interest)
        (steps, path) = self.bfs_b(reduced_graph)
        print(steps, path)
        return steps

        
        

    def part1(self):
        return self.part1b()
    
    def bfs_part2b(self, reduced_graph):
        keys_left = self.keys
        history = {}
        queue = deque()
        print(reduced_graph)
        queue.append(((0,1,2,3), keys_left, 0, []))        
        best_steps = 10000000000
        best_path = None
        while(len(queue)):
            (poi, keys_left, steps, path) = queue.popleft()
            
            if len(keys_left) == 0:  
                if steps < best_steps:
                    best_steps = steps
                    best_path = path
                continue

            keys_hash = list(keys_left)
            keys_hash.sort()
            keys_hash = tuple(keys_hash)
            
            if (poi, keys_hash) in history:
                if history[(poi, keys_hash)] <= steps:
                    continue
            history[(poi, keys_hash)] = steps
            
            for i in range(4):
                pos = poi[i]
                
                for n in reduced_graph[pos]:                
                    if n in self.doors:
                        if n.lower() in keys_left:
                            continue
                    new_poi = list(poi)
                    new_poi[i] = n
                    new_poi = tuple(new_poi)
                    queue.append((new_poi, keys_left - set(str(n)), steps + reduced_graph[pos][n]["weight"], path + [(i,n)]))
        return (best_steps, best_path)

    def bfs_part2d(self, reduced_graph):
        keys_left = get_keys_from_set(self.keys)        
        history = {}
        queue = deque()
        print(reduced_graph)
        queue.append(((0,1,2,3), keys_left, 0, []))        
        best_steps = 10000000000
        best_path = None
        while(len(queue)):
            (poi, keys_left, steps, path) = queue.popleft()            
            if keys_left == 0:  
                if steps < best_steps:
                    best_steps = steps
                    best_path = path
                continue
            
            if (poi, keys_left) in history:
                if history[(poi, keys_left)] <= steps:
                    continue
            history[(poi, keys_left)] = steps
            
            for i in range(4):
                pos = poi[i]
                
                for n in reduced_graph[pos]:                
                    if n in self.doors:
                        if keys_left & (1 << (ord(n) - ord("A"))):
                            continue
                    new_poi = list(poi)
                    new_poi[i] = n
                    new_poi = tuple(new_poi)
                    if n in self.keys:
                        new_keys_left = keys_left ^ get_key_bit(n)
                    else:
                        new_keys_left = keys_left
                    queue.append((new_poi, new_keys_left, steps + reduced_graph[pos][n]["weight"], path + [(i,n)]))

        return (best_steps, best_path)
    

    def bfs_part2(self, maps):
        print(maps)
        keys_left = self.keys
        history = {}
        queue = deque()
        pos = ("@", "@", "@", "@")

        queue.append((pos, keys_left, 0, []))        
        best_steps = 10000000000
        best_path = None
        while(len(queue)):
            (pos, keys_left, steps, path) = queue.popleft()
            
            if len(keys_left) == 0:  
                if steps < best_steps:
                    best_steps = steps
                    best_path = path
                continue

            keys_hash = list(keys_left)
            keys_hash.sort()
            keys_hash = tuple(keys_hash)
            
            if (pos, keys_hash) in history:
                if history[(pos, keys_hash)] <= steps:
                    continue
            history[(pos, keys_hash)] = steps
            
            for i in range(len(maps)):
                local_keys_left = keys_left & maps[i].keys
                if len(local_keys_left) == 0:
                    continue

                for n in maps[i].reduced_graph[pos[i]]:                
                    if n in self.doors:
                        if n.lower() in keys_left:
                            continue                
                    new_pos = list(pos)
                    new_pos[i] = n
                    new_pos = tuple(new_pos)
                    queue.append((new_pos, keys_left - set(n), steps + maps[i].reduced_graph[pos[i]][n]["weight"], path + [(i,n)]))


        return (best_steps, best_path)

    def part2a(self):
        # doesn't work with test case 2_3, but gets the answer
        self.get_pois()
        center = self.points_of_interest["@"]
        self.map[center] = "#"
        for n in center.neighbors():
            self.map[n] = "#"
        for d in [NW, SW, NE, SE]:
            self.map[center + d] = "@"
        
        tl_map = SubMap(self.map.get_sub_map(self.map.corner(NW), center))
        tr_map = SubMap(self.map.get_sub_map(self.map.corner(NE), center))
        bl_map = SubMap(self.map.get_sub_map(self.map.corner(SW), center))
        br_map = SubMap(self.map.get_sub_map(self.map.corner(SE), center))
        maps = [tl_map, tr_map, bl_map, br_map]
        
        (steps, path) = self.bfs_part2(maps)
        print(steps, path)
        return steps
            
    def part2b(self):
        # Slow but works with all test cases ()
        self.get_pois()
        center = self.points_of_interest["@"]
        self.map[center] = "#"
        for n in center.neighbors():
            self.map[n] = "#"
        num = 0
        for d in [NW, SW, NE, SE]:
            self.map[center + d] = num
            num += 1
        reduced_graph = build_reduced_graph(self.map, self.points_of_interest)
        (steps,path) = self.bfs_part2b(reduced_graph)
        return steps

    def part2c_bfs(self, reduced_graph, start):
        keys_left = set()
        for key in self.keys:
            if nx.has_path(reduced_graph, start, key):
                keys_left.add(key)
                
        history = {}
        queue = deque()
        queue.append((start, keys_left, 0, []))
        
        best_steps = 10000000000
        best_path = None
        while(len(queue)):
            (poi, keys_left, steps, path) = queue.popleft()
            
            if len(keys_left) == 0:  
                if steps < best_steps:
                    best_steps = steps
                    best_path = path
                continue

            keys_hash = list(keys_left)
            keys_hash.sort()
            keys_hash = tuple(keys_hash)
            
            if (poi, keys_hash) in history:
                if history[(poi, keys_hash)] <= steps:
                    continue
            history[(poi, keys_hash)] = steps
            
            for n in reduced_graph[poi]:                
                if n in self.doors:
                    if n.lower() in keys_left:
                        continue                                
                queue.append((n, keys_left - set(str(n)), steps + reduced_graph[poi][n]["weight"], path + [n]))
        return (best_steps, best_path)

    def part2c(self):
        # Faster but fails on last test case
        self.get_pois()
        center = self.points_of_interest["@"]
        self.map[center] = "#"
        for n in center.neighbors():
            self.map[n] = "#"
        num = 0
        for d in [NW, SW, NE, SE]:
            self.map[center + d] = num
            num += 1
        reduced_graph = build_reduced_graph(self.map, self.points_of_interest)
        total_steps = 0
        for i in range(4):
            (steps,path) = self.part2c_bfs(reduced_graph, i)
            total_steps += steps
        return total_steps
    
    def part2d(self):
        #Same as 2b but with bitwise key tracking
        self.get_pois()
        center = self.points_of_interest["@"]
        self.map[center] = "#"
        for n in center.neighbors():
            self.map[n] = "#"
        num = 0
        for d in [NW, SW, NE, SE]:
            self.map[center + d] = num
            num += 1
        reduced_graph = build_reduced_graph(self.map, self.points_of_interest)
        (steps,path) = self.bfs_part2d(reduced_graph)
        return steps        

    def part2(self):
        #1816
        return self.part2d()
        


