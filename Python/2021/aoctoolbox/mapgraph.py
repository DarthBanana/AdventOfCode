from Map2D import *
import networkx as nx


class Map2DGraph(nx.Graph):
    def __init__(self, map, valid_values="."):

        self.valid_values = set()
        self.map = map
        super().__init__(self)
        self.add_new_valid_values(valid_values)

    def add_new_valid_values(self, valid_values):
        valid_values = set(valid_values)
        new_values = valid_values - self.valid_values
        self.valid_values = self.valid_values | valid_values

        for coord in self.map:
            if self.map[coord] in new_values:
                for n in coord.neighbor_coords():
                    if self.map[n] in self.valid_values:
                        self.add_edge(coord, n)

    def make_coord_valid(self, coord):
        for n in coord.neighbor_coords():
            if self.map[n] in self.valid_values:
                self.add_edge(coord, n)



def generate_neighbor_graph_from_map(map, valid_values="."):
    graph = nx.Graph()
    for coord in map:
        if map[coord] in valid_values:
            for n in coord.neighbor_coords():
                if map[n] in valid_values:
                    graph.add_edge(coord, n)
    return graph


def update_graph_from_map_with_new_valid_values(map, graph, valid_values):
    for coord in map:
        if map[coord] in valid_values:
            for n in coord.neighbor_coords():
                if map[n] in valid_values:
                    graph.add_edge(coord, n)
    return graph
