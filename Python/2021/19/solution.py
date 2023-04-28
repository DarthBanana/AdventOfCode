## advent of code 2021
## https://adventofcode.com/2021
## day 19

from collections import defaultdict
import copy
from aocpuzzle import *
from CoordND import *

def rotations(coord, i):
            x, y, z = coord.as_tuple()
            rotates = [(x, y, z),
                    (z, y, -x),
                    (-x, y, -z),
                    (-z, y, x),
                    (-x, -y, z),
                    (-z, -y, -x),
                    (x, -y, -z),
                    (z, -y, x),
                    (x, -z, y),
                    (y, -z, -x),
                    (-x, -z, -y),
                    (-y, -z, x),
                    (x, z, -y),
                    (-y, z, -x),
                    (-x, z, y),
                    (y, z, x),
                    (z, x, y),
                    (y, x, -z),
                    (-z, x, -y),
                    (-y, x, z),
                    (-z, -x, y),
                    (y, -x, z),
                    (z, -x, -y),
                    (-y, -x, -z)]
            return CoordND(rotates[i])

class Scanner:
    def __init__(self, lines):
        # first line is ID
        self.id = get_all_ints(lines[0])[0]
        self.beacons = []                
        for line in lines[1:]:
            if len(line) < 3:
                return
            beacon = CoordND(get_all_ints(line))
            self.beacons.append(beacon)            
        self.position = None
        self.orientation = None
        self.translation = CoordND((0,0,0))
        self.build_distances()

    def build_distances(self):
        self.point_distances = defaultdict(set)
        for a in self.beacons:
            for b in self.beacons:
                if a == b:                    
                    continue
                distance = a.distance(b)
                self.point_distances[a].add(distance)                

    def add_beacons(self, beacons):
        for b in beacons:
            if b in self.beacons:
                #print("match:", b)
                continue
            self.beacons.append(b)
        
        self.build_distances()

    def correlate_beacons(self, other):
        mapping = {}
        for b in self.beacons:
            for kb in other.beacons:
                overlap = self.point_distances[b] & other.point_distances[kb]
                if len(overlap) > 10:
                    mapping[b] = kb
                    break      

        for i in range(24):
            x_set = set()
            y_set = set()
            z_set = set()  
            for m in mapping:
                
                rep = rotations(m, i)

                x_set.add(mapping[m][0] - rep[0])
                y_set.add(mapping[m][1] - rep[1])
                z_set.add(mapping[m][2] - rep[2])
            #print("x_set:", x_set, "y_set:", y_set, "z_set:", z_set)
            if len(x_set) == 1 and len(y_set) == 1 and len(z_set) == 1:
                self.orientation = i
                self.translation = CoordND((x_set.pop(), y_set.pop(), z_set.pop()))
                #print("Orientation:", self.orientation)
                #print("Translation:", self.translation)
                break
        assert(self.orientation is not None)
        
        x_set = set()
        y_set = set()
        z_set = set()
        transforms = set()
        for m in mapping:
            new_coord = rotations(m, self.orientation)
            #print("adjusted: ", m, mapping[m], mapping[m] - new_coord)
            transforms.add(mapping[m] - new_coord)
        #print("Transforms:", transforms)
        assert(len(transforms) == 1) 
        self.translation = transforms.pop()
    
    def get_absolute_beacons(self):
        result = []
        for b in self.beacons:
            result.append(rotations(b,self.orientation) + self.translation)
        return result

           
    def get_overlap(self, other):
        result = 0
        for b in self.beacons:
            for kb in other.beacons:
                overlap = self.point_distances[b] & other.point_distances[kb]
                result = max(result, len(overlap))
        return result
    
    def __str__(self):
        return f"Scanner {self.id} at {self.position}"
    
    def __repr__(self):
        return f"Scanner {self.id} at {self.position}"

    def copy(self):
        s = Scanner([])
        s.id = self.id
        s.beacons = self.beacons.copy()
        s.position = self.position
        s.build_distances()
        return s


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.scanners = []
        start_index = None
        end_index = None
        for i in range(len(lines)):            
            if len(lines[i]) < 3:                
                end_index = i
                self.scanners.append(Scanner(lines[start_index:end_index]))
                start_index = None
            elif "scanner" in lines[i]:                
                start_index = i
        if start_index is not None:
            self.scanners.append(Scanner(lines[start_index:]))

        self.virtual_scanner = copy.deepcopy(self.scanners[0])
        self.virtual_scanner.location = CoordND((0,0,0))
                        

    def part1(self):

        candidate_scanners = self.scanners[1:].copy()        
        while(len(candidate_scanners)):
            candidate_scanners.sort(key=lambda x: x.get_overlap(self.virtual_scanner), reverse=True)            
            #print(candidate_scanners)
            scanner = candidate_scanners[0]
            candidate_scanners.remove(scanner)
            #print(scanner.id, scanner.get_overlap(self.virtual_scanner))
            scanner.correlate_beacons(self.virtual_scanner)
            self.virtual_scanner.add_beacons(scanner.get_absolute_beacons())
            #print("Known beacon count: ", len(self.virtual_scanner.beacons))

        #print(self.virtual_scanner.beacons)
        return len(self.virtual_scanner.beacons)                                                   

    def part2(self):
        distance = 0
        for s in self.scanners:
            for other in self.scanners:
                if s.id == other.id:
                    continue
                this_dist = s.translation.distance(other.translation)
                #print("Distance between", s.id, "and", other.id, "is", this_dist)
                distance = max(this_dist, distance)
        return distance
                