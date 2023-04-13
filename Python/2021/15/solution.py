## advent of code 2021
## https://adventofcode.com/2021
## day 15

from aocpuzzle import *
import networkx as nx

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = {}
        y = 0
        self.maxx = 0
        self.maxy = 0
        self.bigmaxx = 0
        self.bigmaxy = 0
        for line in lines:
            self.maxy = max(self.maxy, y)
            x = 0
            for c in line:
                self.maxx = max(self.maxx, x)
                self.map[(x,y)] = int(c) - 1
                x += 1
            y += 1
        self.bigmap = {}

    def part1(self):
        def weight_fn(s,t,e):            
            return self.map[t] + 1

        graph = nx.grid_2d_graph(self.maxx+1, self.maxy+1)        
        path = nx.shortest_path(graph, source=(0,0), target = (self.maxx, self.maxy), weight=weight_fn)
        print(path)
        risk = 0
        for coord in path[1:]:
            risk += self.map[coord]+1
        return risk

    def expand_map(self):
        cy = 0
        dy = 0

        for by in range(5):                        
            for y in range(self.maxy+1):                
                self.bigmaxy = max(self.bigmaxy, cy)
                cx = 0  
                dx = 0              
                for bx in range(5):                
                    for x in range(self.maxx+1):
                        self.bigmaxx = max(self.bigmaxx, cx)
                        v = (self.map[(x,y)] + dx + dy) % 9
                        self.bigmap[(cx,cy)] = v
                        cx += 1
                    dx += 1
                cy += 1
            
            dy += 1


    def part2(self):        
        self.expand_map()

        def weight_fn(s,t,e):            
            return self.bigmap[t] + 1
        
        graph = nx.grid_2d_graph(self.bigmaxx+1, self.bigmaxy+1)
        path = nx.shortest_path(graph, source=(0,0), target = (self.bigmaxx, self.bigmaxy), weight=weight_fn)
        print(path)
        risk = 0
        for coord in path[1:]:
            risk += self.bigmap[coord]+1
        return risk