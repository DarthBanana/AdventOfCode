## advent of code 2019
## https://adventofcode.com/2019
## day 06
import networkx as nx
from aocpuzzle import *
import matplotlib.pyplot as plt

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test = False):
        AoCPuzzle.__init__(self, lines)
        self.orbits = []
        for line in lines:
            self.orbits.append(line.split(')'))
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.orbits)
        #nx.draw(self.graph, pos=nx.kamada_kawai_layout(self.graph), with_labels=True)
        #plt.show()
    def part1(self):
        num_orbits = 0
        for node in self.graph.nodes():            
            num_orbits += nx.shortest_path_length(self.graph, source='COM', target=node)
            
        return num_orbits
    def part2(self):
        return nx.shortest_path_length(self.graph, source='YOU', target='SAN') - 2