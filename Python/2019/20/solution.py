## advent of code 2019
## https://adventofcode.com/2019
## day 20

from collections import deque
from time import sleep
from aocpuzzle import *
from PrettyMap2D import *
from mapgraph import *
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DRAW_RESULT = False
DRAW_RESULT_2 = True

class Puzzle(AoCPuzzle):
    
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = Map2D(default=" ")
        self.map.autodraw = False
        self.map.fill_from_lines(lines)
        self.map.refresh()
        self.map.print()
        self.graph = generate_neighbor_graph_from_map(self.map)
        self.portals = {}
        self.outside_portals = {}
        self.inside_portals = {}
        self.wormholes = {}
        self.find_wormholes()
        self.apply_wormholes()
        self.start = self.portals["AA"][1]
        self.map[self.portals["AA"][0]] = "#"
        self.exit = self.portals["ZZ"][1]
        self.map.print()
            

    def is_portal(self, coord):
        
        for d in NEIGHBORS:
            a = coord
            b = coord + d
            c = b + d
            if self.map[a] in ALPHA:
                if self.map[b] in ALPHA:
                    if self.map[c] == ".":
                        if d == DOWN or d == RIGHT:
                            name = self.map[a] + self.map[b]
                            start = b
                            end = c                            
                        else:
                            name = self.map[b] + self.map[a]
                            start = b
                            end = c                        
                        return (name, start, end)
                            
        return None
        
    def find_wormholes(self):        
        self.pairs = []        
        for a in self.map:
            result = self.is_portal(a)
            if not result:
                continue            
            outside_portal = False
            (name, start, end) = result
            if a.x == self.map.minx or a.x == self.map.maxx or a.y == self.map.miny or a.y == self.map.maxy:
                outside_portal = True

            if name in self.portals:
                (other_start, other_end, outside) = self.portals[name]
                self.wormholes[start] = (outside_portal, other_end)
                self.wormholes[other_start] = (outside, end)
                self.pairs.append((end, other_end))
            else:
                self.portals[name] = (start,end, outside_portal)

    def apply_wormholes(self):
        #for start, end in self.wormholes.items():
            #self.map.create_wormhole(start, end)
        for p in self.pairs:
            self.graph.add_edge(p[0], p[1])


    def part1(self):
        path = nx.shortest_path(self.graph, self.start, self.exit)
        if DRAW_RESULT:
            self.map.autodraw = True
            overlay = self.map.add_overlay(100)
            for p in path:
                overlay[p] = "o"
            while(True):
                self.map.refresh()
        return len(path) - 1
    
    def p2_bfs(self):
        last = -2
        goal = (0, self.exit)
        location = (0,self.start)        
        queue = deque()
        visited = {}
        queue.append((location, 0, []))
        while (len(queue) > 0):
            (location, steps, path) = queue.popleft()
            if steps > last:
                print(steps)
            last = steps
            #print(location)
            if location[0] == 0 and location[1] == self.exit:
                print("found it!")
                print(path)
                            
                return steps, path

            if location in visited:
                if visited[location] <= steps:
                    continue
            visited[location] = steps
            for (n,_) in self.map.valid_neighbors(location[1]):
                if n == self.exit:
                    if location[0] != 0:
                        continue

                #print(location, n)
                new_layer = location[0]
                if n in self.wormholes:
                    #print("Wormhole!")
                    #print(self.wormholes[n])            
                    
                    if self.wormholes[n][0]:
                        #print("Ouside Wormhole!")
                        new_layer = location[0] - 1                        
                        if new_layer < 0:
                            continue
                    else:
                        #print("Inside Wormhole!")
                        new_layer = location[0] + 1
                    n = self.wormholes[n][1]    
                new_location = (new_layer, n)
                assert(self.map[n] == ".")
                queue.append((new_location, steps + 1, path + [new_location]))
        assert(False)

    def part2(self):
        (steps, path) = self.p2_bfs()
        
        return steps
        