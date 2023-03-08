from enum import Enum
import itertools
import sys



class Coord2D:
    def __init__(self, x=0,y=0):
        self.x = int(x)
        self.y = int(y)        
    
    def manhattan_dist(self, other):
        return abs((self.x - other.x)) + abs((self.y - other.y))

    def dist(self, other):
        return self.manhattan_dist(other)
    def distance(self, other):
        return self.manhattan_dist(other)
    def as_tuple(self):
        return (self.x, self.y)
    
    def __mul__(self, other):
        return Coord2D(self.x * other, self.y*other)
    def __rmul__(self, other):
        return Coord2D(self.x * other, self.y*other)
    def __add__(self, other):
        return Coord2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Coord2D(self.x - other.x, self.y - other.y)
    def __truediv__(self, other):
        return Coord2D(self.x / other, self.y / other)
    def __floordiv__(self, other):
        return Coord2D(self.x // other, self.y // other)
    def __mod__(self, other):
        return Coord2D(self.x % other, self.y % other)

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)
    
    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)

    def __hash__(self):
        return hash(self.as_tuple())
    def __eq__(self, other):
        return ((self.x == other.x) and (self.y == other.y))
    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y == other.y:
            return (self.x < other.x)
        else:
            return False

    def surrounding_coords(self):
        return [Coord2D(self.x + i.x, self.y + i.y) for i in SURROUNDING]
    
    def neighbor_coords(self):
        return [Coord2D(self.x + i.x, self.y + i.y) for i in NEIGHBORS]
    def neighbors(self):
        return [(self + i) for i in NEIGHBORS]

    def rectangle_tl_coords(self, width, height):
        for y in range(self.y, self.y+height):
            for x in range(self.x, self.x+width):            
                yield Coord2D(x,y)


class Direction(Coord2D):
    def __init__(self, direction):
        Coord2D.__init__(self, direction.x, direction.y)
    def __str__(self):
        return DIRECTION_STRINGS[self]
    def __repr__(self):
        return DIRECTION_STRINGS[self]
    def turn(self, degrees):
        if degrees % 45 != 0:
            raise Exception("Can only turn in 45 degree increments")
        steps = degrees // 45
        index = SURROUNDING.index(self)
        assert(SURROUNDING[index] == self)
        index = ((index + len(SURROUNDING)) + steps) % len(SURROUNDING)
        new_dir = SURROUNDING[index]
        self.x = new_dir.x
        self.y = new_dir.y

    def turn_left_90(self):
        self.turn(-90)
    def turn_right_90(self):
        self.turn(90)
    def turn_180(self):
        self.turn(180)
    
UP = Direction(Coord2D(0,-1))
DOWN = Direction(Coord2D(0, 1))
LEFT = Direction(Coord2D(-1, 0))
RIGHT = Direction(Coord2D(1, 0))
N = UP
S = DOWN
E = RIGHT
W = LEFT
NE = Direction(Coord2D(1, -1))
SE = Direction(Coord2D(1, 1))
SW = Direction(Coord2D(-1, 1))
NW = Direction(Coord2D(-1, -1))

DIRECTION_STRINGS = {
    N: "N",
    S: "S",
    E: "E",
    W: "W",
    NE: "NE",
    SE: "SE",
    SW: "SW",
    NW: "NW"
}



SURROUNDING = [N, NE, E, SE, S, SW, W, NW]
NEIGHBORS = [N, E, S, W]
def TurnLeft90(Direction):
    index = SURROUNDING.index(Direction)
    assert(SURROUNDING[index] == Direction)
    index = ((index + len(SURROUNDING)) - 2) % len(SURROUNDING)
    return SURROUNDING[index]
def TurnRight90(Direction):
    index = SURROUNDING.index(Direction)
    assert(SURROUNDING[index] == Direction)
    index = (index + 2) % len(SURROUNDING)
    return SURROUNDING[index]
    


class PerimeterType(Enum):
    NONE = 1
    RECTANGLE = 2
    
class InfiniteGrid:
    def __init__(self, default = 0):
        self.map = {}
        self.default = default
        self.minx = sys.maxsize
        self.maxx = -sys.maxsize - 1
        self.miny = sys.maxsize
        self.maxy = -sys.maxsize -1 
        self.perimeter_type = PerimeterType.NONE
    def __iter__(self):
        return self.map.__iter__()

    def fill_from_lines(self, lines):
        y = 0
        for line in lines:
            x = 0
            for c in line:
                self[Coord2D(x,y)] = c
                x += 1
            y += 1
    def is_out_of_bounds(self, coord):
        if self.perimeter_type == PerimeterType.RECTANGLE:        
            if (coord.x <= (self.perimeter_minx)) or (coord.x >= (self.perimeter_maxx)) or (coord.y <= (self.perimeter_miny)) or (coord.y >= (self.perimeter_maxy)):                
                return True
        return False

    def __getitem__(self, k):        
        if self.is_out_of_bounds(k):
            return self.perimeter_value
        return self.map.get(k, self.default)

    def __setitem__(self, k, value):        
        if self.is_out_of_bounds(k):            
            return
    
        self.minx = min(self.minx, k.x)
        self.maxx = max(self.maxx, k.x)
        self.miny = min(self.miny, k.y)
        self.maxy = max(self.maxy, k.y)
        self.map[k] = value
    def __hash__(self):
        return hash(frozenset(self.map.items()))
    def __len__(self):
        return len(self.map)
    def get_width(self):
        return (self.maxx + 1) - self.minx
    def get_height(self):
        return (self.maxy + 1) - self.miny
    def print(self, offset=0, max_y_size = 1000, max_x_size = 1000, default="."):

        print()
        y_range = range(self.miny-offset, self.maxy + 1 + offset)
        x_range = range(self.minx-offset, self.maxx + 1+offset)
        if len(y_range) > max_y_size:
            print("Y too big")
            return
        if len(x_range) > max_x_size:
            print("X too big")
            return
        for y in y_range:
            for x in x_range:
                coord = Coord2D(x,y)
                #if coord in self.map.keys():
                print(self[coord], end="")
                #else:
                #    print(default, end="")
            print()
    

    def set_auto_rectangle_perimeter(self, value, offset=1):
        self.perimeter_type = PerimeterType.RECTANGLE        
        self.perimeter_value = value
        self.perimeter_minx = self.minx - offset
        self.perimeter_maxx = self.maxx + offset
        self.perimeter_miny = self.miny - offset
        self.perimeter_maxy = self.maxy + offset
    def set_rectangle_perimeter(self, value, minx, miny, maxx, maxy):
        self.perimeter_type = PerimeterType.RECTANGLE        
        self.perimeter_value = value
        self.perimeter_minx = minx
        self.perimeter_maxx = maxx
        self.perimeter_miny = miny
        self.perimeter_maxy = maxy
    def rectangle_coords(self, offset = 0):
        if self.perimeter_type == PerimeterType.RECTANGLE:
            minx = self.perimeter_minx + 1
            miny = self.perimeter_miny + 1
            maxx = self.perimeter_maxx - 1
            maxy = self.perimeter_maxy - 1
        else:
            minx = self.minx
            miny = self.miny
            maxx = self.maxx
            maxy = self.maxy

        for y in range(miny - offset, maxy+1 + offset):
            for x in range(minx - offset, maxx + 1 + offset):
                yield Coord2D(x,y)

    def is_boundary(self, coord, offset = 0):
        if self.perimeter_type == PerimeterType.RECTANGLE:
            minx = (self.perimeter_minx + 1) - offset
            miny = (self.perimeter_miny + 1) - offset
            maxx = (self.perimeter_maxx - 1) + offset
            maxy = (self.perimeter_maxy - 1) + offset
        else:
            minx = self.minx - offset
            miny = self.miny - offset
            maxx = self.maxx + offset
            maxy = self.maxy + offset

        if (coord.x == minx) or (coord.x == maxx) or (coord.y == miny) or (coord.y == maxy):
            return True
        return False

def rectangle_coords(x,y,width,height):
    for y1 in range(y, y+height):
        for x1 in range(x, x+width):            
            yield Coord2D(x1,y1)

def surrounding_coords(x,y):
    return [Coord2D(x + i.x, y + i.y) for i in SURROUNDING]
    
def neighbor_coords(x,y):
    return [Coord2D(x + i.x, y + i.y) for i in NEIGHBORS]


#def surrounding_coords(x, y):
#    return [Coord2D(x + i.x, y + i.y) for i in SURROUNDING]
    
#def neighbor_coords(x,y):
#    return [Coord2D(x + i.x, y + i.y) for i in NEIGHBORS]

def build_min_distances(valid_coords):
    distances = {}
    for coord in valid_coords:
        distances[(coord,coord)] = 0
        for n in coord.neighbor_coords():
            if n in valid_coords:
                distances[(coord, n)] = 1
    
    for k in valid_coords:
        for i in valid_coords:
            for j in valid_coords:
                if (i,k) in distances:
                    dist_ik = distances[(i,k)]
                else:
                    continue
                if (k,j) in distances:
                    dist_kj = distances[(k,j)]
                else:
                    continue
                if (i,j) in distances:
                    dist_ij = min(distances[i,j], dist_ik + dist_kj)
                else:
                    dist_ij = dist_ik + dist_kj
                distances[(i,j)] = dist_ij
    return distances
def find_distances_from_coord(valid_coords, coord):
    distances = {}
    for c in valid_coords:
        distances[c] = 0
    distances[coord] = 0
    queue = [coord]
    while len(queue) > 0:
        c = queue.pop(0)
        for n in c.neighbor_coords():
            if n in valid_coords:
                if distances[n] == 0:
                    distances[n] = distances[c] + 1
                    queue.append(n)
    return distances