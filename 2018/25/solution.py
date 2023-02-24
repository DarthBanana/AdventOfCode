## advent of code 2018
## https://adventofcode.com/2018
## day 25
import networkx as nx
from matplotlib import pyplot as plt
from CoordND import *
class Puzzle:
    def __init__(self, lines):
        self.points = []
        for line in lines:
            coord = CoordND((int(x) for x in line.split(',')))
            self.points.append(coord)
        

    def part1(self):
        G = nx.Graph()
        labels = {}
        for i in range(len(self.points)):
            G.add_node(i)
            for j in range(i+1, len(self.points)):
                p1 = self.points[i]
                p2 = self.points[j]                
                if p1.distance(p2) <= 3:                
                    G.add_edge(i, j, weight=p1.distance(p2))
                    labels[(i,j)] = str(p1.distance(p2))
                
        return len(list(nx.connected_components(G)))  

    def part2(self):
        pass