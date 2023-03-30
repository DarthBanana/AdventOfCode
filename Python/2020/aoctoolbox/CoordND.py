from enum import Enum
from itertools import *

def adjac(ele, sub = ()):
    if not ele:
        yield sub
    else:
        yield from (idx for j in range(ele[0] - 1, ele[0] + 2)
            for idx in adjac(ele[1:], sub + (j,)))

def dim_iterator(ele, dim, sub = ()):    
    if not ele:
        yield sub
    else:
        yield from (idx for j in range(ele[0], ele[0] + dim[0]+ 1)
            for idx in dim_iterator(ele[1:], dim[1:], sub + (j,)))

class CoordND:
    def __init__(self, coord):
        self.coord = tuple(coord)
    
    def min(self, other):
        if other is None:
            return self.copy()
        return CoordND(tuple(map(lambda i, j: min(i, j), self.coord, other.coord)))
    def max(self, other):
        if other is None:
            return self.copy() 
        return CoordND(tuple(map(lambda i, j: max(i, j), self.coord, other.coord)))
    
    def manhattan_distance(self, other=None):
        if other is None:
            return sum(abs(value) for value in self.coord)
        return sum(abs(value1 - value2) for value1, value2 in zip(self.coord, other.coord))        
    manhattan_dist = manhattan_distance
    dist = manhattan_distance
    distance = manhattan_distance
    def as_tuple(self):
        return self.coord
    
    def __mul__(self, other):
        return CoordND(tuple(map(lambda i: i * other, self.coord)))
    
    def __imul__(self, other):
        self.coord = tuple(map(lambda i: i * other, self.coord))
        return self
        
    def __rmul__(self, other):
        return CoordND(tuple(map(lambda i: i * other, self.coord)))
    
    def __irmul__(self, other):
        self.coord = tuple(map(lambda i: i * other, self.coord))
        return self

    def __add__(self, other):
        return CoordND(tuple(map(lambda i, j: i + j, self.coord, other.coord)))
    
    def __iadd__(self, other):
        self.coord = tuple(map(lambda i, j: i + j, self.coord, other.coord))
        return self
    
    def __sub__(self, other):
        return CoordND(tuple(map(lambda i, j: i - j, self.coord, other.coord)))
    
    def __isub__(self, other):
        self.coord = tuple(map(lambda i, j: i - j, self.coord, other.coord))
        return self
    
    def __truediv__(self, other):
        return CoordND(tuple(map(lambda i: i / other, self.coord)))
    
    def __itruediv__(self, other):
        self.coord = tuple(map(lambda i: i / other, self.coord))
        return self
    
    def __floordiv__(self, other):
        return CoordND(tuple(map(lambda i: i // other, self.coord)))
    
    def __ifloordiv__(self, other):
        self.coord = tuple(map(lambda i: i // other, self.coord))
        return self
    
    def __mod__(self, other):
        return CoordND(tuple(map(lambda i: i % other, self.coord)))
    
    def __imod__(self, other):
        self.coord = tuple(map(lambda i: i % other, self.coord))
        return self

    def __str__(self):        
        return str(self.coord)
    
    def __repr__(self):
        return str(self.coord)

    def __hash__(self):
        return hash(self.as_tuple())
    
    def __eq__(self, other):
        return self.coord == other.coord
        
    def __lt__(self, other):
        for i in range(len(self.coord)):
            if self.coord[-i] < other.coord[-i]:
                return True
            if self.coord[-i] > other.coord[-i]:
                return False
        return False
    
    def __getitem__(self, k):        
        return self.coord[k]

    def __setitem__(self, k, value):       
        coords = list(self.coord) 
        coords[k] = value
        self.coord = tuple(coords)

    def __len__(self):
        return len(self.coord)
  
    def surrounding_coords(self):
        coords = []
        for i in adjac(self.coord):
            if i != self.coord:
                coords.append(CoordND(i))
        #coords.sort()
        return coords
    
    def neighbor_coords(self):
        coords = []
        for i in range(len(self.coord)):
            coord = list(self.coord)
            coord[i] += 1
            coords.append(CoordND(coord))
            coord[i] -= 2
            coords.append(CoordND(coord))
        coords.sort()
        return coords
        
    def neighbors(self):
        return self.neighbor_coords(self)

    def rectangle_tl_coords(self, dims):
        for i in dim_iterator(self.coord, dims):
            yield CoordND(i)
    
    def copy(self):
        return CoordND(self.coord)
        
    
