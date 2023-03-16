# advent of code 2019
# https://adventofcode.com/2019
# day 18

from collections import deque
import copy
from Map2D import Map2D
from aocpuzzle import *
from mapgraph import *


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.map = Map2D()
        self.map.fill_from_lines(lines)
        self.map.print()
        self.points_of_interest = {}
        self.keys = set()
        self.doors = set()
        self.graph = Map2DGraph(self.map, r"abcdefghijklmnopqrstuvwxyz@ABCDEFGHIJKLMNOPQRSTUVWXYZ.")
        self.graphs = {}
        self.shortest_path = 9999999999999

    def get_next_key(self, pos, found_keys, graph, steps):
        print(found_keys, steps, self.shortest_path)
        keys_left = self.keys - found_keys
        # print(keys_left)
        if len(keys_left) == 0:
            if steps < self.shortest_path:
                self.shortest_path = steps
                print(steps)
        if steps > self.shortest_path:
            return

        keys = []
        for key in keys_left:
            if nx.has_path(graph, pos, self.points_of_interest[key]):
                distance = nx.shortest_path_length(graph,
                                                   pos, self.points_of_interest[key])
                keys.append((key, distance))
        keys.sort(key=lambda x: x[1])

        for (key,distance) in keys:
            # print(distance)
            new_graph = copy.deepcopy(graph)
            if key.upper() in self.points_of_interest:
                new_graph.make_coord_valid(
                    self.points_of_interest[key.upper()])
            self.get_next_key(self.points_of_interest[key], found_keys | set(
                key), new_graph, steps + distance)
            
    def get_graph_for_keys(self, keys):
        key_hash = list(keys)
        key_hash.sort()
        key_hash = tuple(key_hash)
        if key_hash in self.graphs:
            return self.graphs

        graph = copy.deepcopy(self.graph)
        remaining_keys = self.keys - keys
        for key in remaining_keys:
            graph.remove_node()

    def bfs_search(self):
        keys_left = self.keys
        pos = self.points_of_interest["@"]
        history = {}
        queue = []
        queue.append((pos, keys_left, 0, []))
        while(len(queue)):
            
            queue.sort(key=lambda x: x[2], reverse=True)
            (pos, keys_left, steps, path) = queue.pop()
            keys_left_hash = list(keys_left)
            keys_left_hash.sort()
            keys_left_hash = tuple(keys_left_hash)
            if (pos, keys_left_hash) in history:
                if steps >= history[(pos, keys_left_hash)]:
                    continue
            history[(pos, keys_left_hash)] = steps
            print(keys_left, steps)
            if len(keys_left) == 0:
                return steps, path
            
            graph = copy.deepcopy(self.graph)
            keys_found = self.keys - keys_left
            for key in keys_found:
                if (key.upper() in self.points_of_interest):
                    graph.make_coord_valid(self.points_of_interest[key.upper()])

            for key in keys_left:
                #print("trying next key ", key)
                if nx.has_path(graph, pos, self.points_of_interest[key]):
                    #print("found path to ", key)
                    distance = nx.shortest_path_length(graph, pos, self.points_of_interest[key])
                    queue.append((self.points_of_interest[key], keys_left - set(key), steps + distance, path + [key]))

        assert(False)
    def get_pois(self):
        for coord in self.map:
            value = self.map[coord]
            if value == "." or value == "#":
                continue
            self.points_of_interest[value] = coord
            if value in "abcdefghijklmnopqrstuvwxyz":
                self.keys.add(value)
            if value in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                self.doors.add(value)

    def part1a(self):
        self.get_pois()
        print(self.points_of_interest)
        print(self.keys)
        steps, path = self.bfs_search()
        print(steps, path)
        #self.get_next_key(self.points_of_interest["@"], set(), self.graph, 0)
        return steps
                

    def get_paths_from_point(self, poi):
        pos = self.points_of_interest[poi]
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
            value = self.map[pos]
            if value != "." and value != poi:
                paths[value] = dist
                continue
            for n in pos.neighbors():
                if self.map[n] == "#":
                    continue
                queue.append((n, dist+1))
        return paths

    def build_reduced_graph(self):
        reduced_graph = nx.Graph()
        for p in self.points_of_interest:
            paths = self.get_paths_from_point(p)
            for d in paths:
                reduced_graph.add_edge(p, d, weight=paths[d])

        return reduced_graph

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
        reduced_graph = self.build_reduced_graph()
        (steps, path) = self.bfs_b(reduced_graph)
        print(steps, path)
        return steps

        
        

    def part1(self):
        return self.part1b()

    def part2(self):
        pass
