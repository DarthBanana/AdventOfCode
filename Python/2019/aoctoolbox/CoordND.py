from enum import Enum
import itertools
import sys


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
    
    def manhattan_dist(self, other):
        return sum(abs(value1 - value2) for value1, value2 in zip(self.coord, other.coord))        

    def dist(self, other):
        return self.manhattan_dist(other)
    def distance(self, other):
        return self.manhattan_dist(other)
    def as_tuple(self):
        return self.coord
    
    def __mul__(self, other):
        return CoordND(tuple(map(lambda i: i * other, self.coord)))
        
    def __rmul__(self, other):
        return CoordND(tuple(map(lambda i: i * other, self.coord)))
    def __add__(self, other):
        return CoordND(tuple(map(lambda i, j: i + j, zip(self.coord, other.coord))))
    def __sub__(self, other):
        return CoordND(tuple(map(lambda i, j: i - j, zip(self.coord, other.coord))))
    def __truediv__(self, other):
        return CoordND(tuple(map(lambda i: i / other, self.coord)))
    def __floordiv__(self, other):
        return CoordND(tuple(map(lambda i: i // other, self.coord)))
    def __mod__(self, other):
        return CoordND(tuple(map(lambda i: i % other, self.coord)))

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
  
    def surrounding_coords(self):
        coords = [CoordND(i) for i in adjac(self.coord)]
        coords.sort()
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
        
    
