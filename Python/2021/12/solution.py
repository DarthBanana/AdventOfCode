## advent of code 2021
## https://adventofcode.com/2021
## day 12

from collections import deque
from aocpuzzle import *
import networkx as nx

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.reset()

    def reset(self):
        self.graph = nx.Graph()
        self.small_rooms = set()
        for line in self.lines:
            a, b = line.split("-")
            self.graph.add_edge(a, b)
            if a.islower() and a != "start" and a != "stop":
                self.small_rooms.add(a)
            if b.islower() and b != "start" and b != "stop":
                self.small_rooms.add(b)
        

    def bfs(self, small_cave_revisit=False):
        queue = deque()        
        queue.append(("start", ["start"], not small_cave_revisit))
        paths = []
        while(queue):
            node, path, revisited = queue.popleft()
            if node == "end":
                #print(path)
                paths.append(path)
                continue
            for n in self.graph.neighbors(node):
                if n in path:
                    if n in self.small_rooms and revisited == False:
                        queue.append((n, path + [n], True))
                        continue
                    elif n.islower():                          
                        continue

                queue.append((n, path + [n], revisited))
        return len(paths)



    def part1(self):
        return self.bfs()
    def part2(self):
        return self.bfs(True)