## advent of code 2018
## https://adventofcode.com/2018
## day 22
import networkx as nx


from collections import deque
from Map2D import *

TOOLS = {'.': ['torch', 'climbing gear'], '=': ['climbing gear', 'neither'], '|': ['torch', 'neither']}
class Puzzle:
    def __init__(self, lines):
        self.depth = int(lines[0].split(' ')[1])
        self.target = Coord2D(*map(int, lines[1].split(' ')[1].split(',')))
        self.erosion_map = InfiniteGrid()
        self.shortest_path = sys.maxsize
        self.visited = {}

    def get_erosion_level(self, coord, depth = 0):

        if depth > 100:
            print("TOO DEEP")
            assert(False)
        if coord in self.erosion_map.map.keys():
            return self.erosion_map[coord]
            
        self.get_geo_index(coord, depth + 1)
        level = (self.get_geo_index(coord, depth + 1) + self.depth) % 20183
        self.erosion_map[coord] = level
        return level
        

    def get_geo_index(self, coord, depth = 0):      
        assert(coord.x >= 0) 
        assert(coord.y >= 0)  
        if coord == Coord2D(0,0):
            return 0
        if coord == self.target:
            return 0
        if coord.y == 0:
            return coord.x * 16807
        if coord.x == 0:
            return coord.y * 48271
        return self.get_erosion_level(coord + LEFT, depth + 1) * self.get_erosion_level(coord + UP, depth + 1)
        
    
    def get_type(self, coord):
        value = self.get_erosion_level(coord) % 3
        if value == 0:
            return '.' # rocky  - no risk
        if value == 1:
            return '=' # wet    - medium risk
        if value == 2:
            return '|' # narrow - high risk

    def build_cave_map(self, coord):
        for coord in Coord2D(0,0).rectangle_tl_coords(self.target.x + 1, self.target.y + 1):
            self.cave_map[coord] = self.get_type(coord)

    def build_erosion_map(self, coord):
        for coord in Coord2D(0,0).rectangle_tl_coords(coord.x + 1, coord.y + 1):
            self.erosion_map[coord] = self.get_erosion_level(coord)

    def get_risk_level(self):
        risk = 0
        for coord in Coord2D(0,0).rectangle_tl_coords(self.target.x + 1, self.target.y + 1):
                 
            if self.get_type(coord) == '=':
                risk += 1
            if self.get_type(coord) == '|':
                risk += 2
        return risk

    def is_tool_allowed(self, coord, tool):
        assert(coord.x >= 0)
        assert(coord.y >= 0)
        if self.get_type(coord) == '.':
            return tool in ['torch', 'climbing gear']
        if self.get_type(coord) == '=':
            return tool in ['climbing gear', 'neither']
        if self.get_type(coord) == '|':
            return tool in ['torch', 'neither']


    def build_3d_graph(self, lr_coord):
        graph = nx.Graph()
        for coord in Coord2D(0,0).rectangle_tl_coords(lr_coord.x + 1, lr_coord.y + 1):
            tools = TOOLS[self.get_type(coord)]
            graph.add_edge((coord, tools[0]), (coord, tools[1]), weight=7)
            for c in coord.neighbors():
                if c.x < 0 or c.y < 0:
                    continue
                if c.x > lr_coord.x or c.y > lr_coord.y:
                    continue
                ntools = TOOLS[self.get_type(c)]
                for tool in tools:
                    if tool in ntools:
                        graph.add_edge((coord, tool), (c, tool), weight=1)
        return graph

        

    def part1(self):       
        self.build_erosion_map(self.target) 
        return self.get_risk_level()

    def part2(self):
        lr_coord = self.target + SE * 100
        self.build_erosion_map(lr_coord) 
        graph = self.build_3d_graph(lr_coord)
        self.shortest_path = nx.dijkstra_path_length(graph, (Coord2D(0,0), 'torch'), (self.target, 'torch'))
        return self.shortest_path