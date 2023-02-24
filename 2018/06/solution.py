## advent of code 2018
## https://adventofcode.com/2018
## day 06
from collections import deque
import re
from Map2D import *
point_re = re.compile(r"(\d+), (\d+)")
class Puzzle:
    def __init__(self, lines):
        self.grid = InfiniteGrid((0,0))
        self.points = []
        id = 0
        for line in lines:
            id += 1
            match = point_re.search(line)
            coord = Coord2D(int(match.group(1)), int(match.group(2)))
            self.points.append((id, coord))            
            self.grid[coord] = (id, 0)
        self.grid.set_rectangle_perimeter((-1,0), 2)
        self.candidates = set()        

    def alt_part1(self):
        candidates = {}
        for point, coord in self.points:
            candidates[point] = 0
        
        for coord in self.grid.rectangle_coords():
            distances = []
            min_distances = []
            min_distance = 100000000            
            for point, point_coord in self.points:
                dist = coord.manhattan_dist(point_coord)                
                if dist < min_distance:
                    #print(min_distance, dist)
                    min_distances = [point]
                    #print(min_distances)
                    min_distance = dist
                elif dist == min_distance:                    
                    min_distances.append(point)
                    #print(min_distance, dist)
                    #print(min_distances)
                       
            if len(min_distances) > 1:
                self.grid[coord] = 0                
            else:                
                point = min_distances[0]
                self.grid[coord] = point                
                if point in candidates.keys():
                    candidates[point] = candidates[point] + 1
                
                if self.grid.is_boundary(coord):                                    
                    candidates.pop(point, None)
                    #if point in candidates.keys():
                    #    candidates.delete(point)

        return max(candidates.values())

        
    def grow_areas(self):
        self.candidates = set()
        queue = deque()
        for point, coord in self.points:            
            queue.append((point, coord, 0))
            self.candidates.add(point)

        while(queue):

            #print("length ", len(queue))
            point, coord, depth = queue.popleft()

            #print(point, coord, depth)                        
            existing_id, existing_depth = self.grid[coord]  
            #print(existing_id, existing_depth)          
            if depth > 0:
                if existing_id == 0:
                    #print("new")
                    self.grid[coord] = (point, depth)                            
                elif (existing_id == point):
                    #print("already mine")
                    continue
                elif existing_depth == depth:    
                    #print("collision")
                    self.grid[coord] = (-2, existing_depth)
                    continue
                else:
                    #print("other")
                    continue


            for neighbor in neighbor_coords(coord):   
                next_id, existing_depth = self.grid[neighbor]  
                #print(neighbor, next_id)              
                if next_id == 0:            
                    #print("adding ", point, neighbor)        
                    queue.append((point, neighbor, depth + 1))
                elif next_id == -1:
                    if point in self.candidates:
                        self.candidates.remove(point)
                elif (next_id > 0) and not (next_id == point):
                    assert(existing_depth < depth + 1)


    def find_largest_area(self):
        largest_area = 0
        for point in self.candidates:            
            area = len(list(filter(lambda m:m[0] == point, self.grid.map.values())))
            #print(point, area)
            largest_area = max(largest_area, area)
        return largest_area

    def part1(self):
        #self.grow_areas()
        
        #return self.find_largest_area()
        return self.alt_part1()

    def part2(self):
        if len(self.points) > 10:
            threshold = 10000
        else:
            threshold = 32
        points = 0
        for coord in self.grid.rectangle_coords():
            dist = 0
            for point, point_coord in self.points:
                dist += coord.manhattan_dist(point_coord)                
            if dist < threshold:
                points += 1                
        return points
        