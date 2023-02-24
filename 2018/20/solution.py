## advent of code 2018
## https://adventofcode.com/2018
## day 20

from Map2D import *
class Puzzle:
    def __init__(self, lines):
        self.map = InfiniteGrid("#")
        self.path = lines[0]
        self.min_distances = {}

    def move(self, coord, direction):
        if direction == "N":
            coord = coord + N
            self.map[coord] = "-"
            coord = coord + N
            self.map[coord] = "."
        elif direction == "S":
            coord = coord + S
            self.map[coord] = "-"
            coord = coord + S
            self.map[coord] = "."
        elif direction == "E":
            coord = coord + E
            self.map[coord] = "|"
            coord = coord + E
            self.map[coord] = "."
        elif direction == "W":
            coord = coord + W
            self.map[coord] = "|"
            coord = coord + W
            self.map[coord] = "."

        return coord


    def follow_path(self, coords, index):
        
        while True:
            c = self.path[index]
            if c == ")":
                return index, coords
            if c == "|":
                return index, coords
            if c == "(":
                index, coord = self.follow_options(coords, index)
                continue
            if c == "$":
                return index, coords
            next_coords = []
            for coord in coords:
                next_coords.append(self.move(coord, c))
            coords = next_coords            
            index += 1

    def follow_options(self, coords, index):
        next_coords = []
        while True:
            c = self.path[index]            
            if c == ")":
                index += 1
                return index, coords
            elif c == "|":
                index += 1
                index, sub_coords = self.follow_path(coords, index)
                next_coords.append(sub_coords)
            elif c == "(":
                index += 1
                index, sub_coords = self.follow_path(coords, index)
                next_coords.append(sub_coords)
            else:
                assert(False)            
        
        
    def walk_map(self, coord):
        coords = [coord]
        self.follow_path(coords, 0)

    def compute_distances(self):
        points = set()
        for coord in self.map.rectangle_coords():
            
            if not self.map[coord] == "#":
                points.add(coord)
        
        self.min_distances = find_distances_from_coord(points, Coord2D(0,0))
    
    def part1(self):
        self.walk_map(Coord2D(0,0))
        self.compute_distances()
        
        max_distance = (max(self.min_distances.values()) + 1) // 2
        
        return max_distance

    def part2(self):
        total = 0
        print(len(self.min_distances.values()))
        for coord, dist in self.min_distances.items():
            if self.map[coord] == ".":
                dist = (dist + 1) // 2
                if dist >= 1000:
                    total += 1
        return total