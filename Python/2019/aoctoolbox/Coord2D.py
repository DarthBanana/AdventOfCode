from enum import Enum
from CoordND import CoordND


class Coord2D(CoordND):
    def __init__(self, x=0,y=0):
        self.x = int(x)
        self.y = int(y) 
        CoordND.__init__(self, [self.x, self.y]) 
    
    def manhattan_distance(self, other):
        return abs((self.x - other.x)) + abs((self.y - other.y))

    def as_tuple(self):
        return (self.x, self.y)
    
    def __mul__(self, other):
        return Coord2D(self.x * other, self.y*other)
    
    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self
    
    def __rmul__(self, other):
        return Coord2D(self.x * other, self.y*other)
    
    def __irmul__(self, other):
        self.x *= other
        self.y *= other
        return self
    
    def __add__(self, other):
        return Coord2D(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        return Coord2D(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __truediv__(self, other):
        return Coord2D(self.x / other, self.y / other)
    
    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self
    
    def __floordiv__(self, other):
        return Coord2D(self.x // other, self.y // other)
    
    def __ifloordiv__(self, other):
        self.x //= other
        self.y //= other
        return self
    
    def __mod__(self, other):
        return Coord2D(self.x % other, self.y % other)
    
    def __imod__(self, other):
        self.x %= other
        self.y %= other
        return self

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
        
    def __gt__(self, other):
        if self.y > other.y:
            return True
        elif self.y == other.y:
            return (self.x > other.x)
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
        print(SURROUNDING)
        if degrees % 45 != 0:
            raise Exception("Can only turn in 45 degree increments")
        steps = degrees // 45
        index = SURROUNDING.index(self)
        print(index)
        print(SURROUNDING[index])
        assert(SURROUNDING[index] == self)
        index = ((index + len(SURROUNDING)) + steps) % len(SURROUNDING)
        print(index)
        new_dir = SURROUNDING[index]
        print(SURROUNDING[index])

        print("Turning {0} degrees from {1} to {2}".format(degrees, self, new_dir))
        
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
    