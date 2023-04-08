from enum import Enum
from Coord2D import *

import sys


class PerimeterType(Enum):
    NONE = 1
    RECTANGLE = 2


class Map2DOverlay:
    def __init__(self, map, altitude):
        self.attached_map = map
        self.altitude = altitude
        self.map = {}

    def clear(self):
        self.map.clear()

    def __getitem__(self, k):
        return self.map.get(k, None)

    def __setitem__(self, k, value):
        self.map[k] = value

    def __contains__(self, k):
        return k in self.map


class PointerOverlay(Map2DOverlay):

    def __init__(self, map):
        self.attached_map = map
        self.coord = None
        self.value = None

    def __setitem__(self, k, value):
        self.coord = k
        self.value = value

    def __getitem__(self, k):
        if k == self.coord:
            return self.value
        else:
            return None

    def clear(self):
        self.coord = None
        self.value = None

    def __contains__(self, k):
        return k == self.coord


class Map2D:
    def __init__(self, default=None, lines=None):

        self.default = default

        self.perimeter_type = PerimeterType.NONE
        self.overlays = []
        self.pointer_overlay = None
        self.invalid = set("#")
        self.wormholes = {}
        self.clear()
        if lines:
            self.fill_from_lines(lines)

    def copy(self):
        new_map = Map2D(self.default)
        new_map.map = self.map.copy()
        new_map.minx = self.minx
        new_map.maxx = self.maxx
        new_map.miny = self.miny
        new_map.maxy = self.maxy
        new_map.perimeter_type = self.perimeter_type
        new_map.invalid = self.invalid.copy()
        new_map.wormholes = self.wormholes.copy()
        return new_map


    def refresh(self):
        pass

    def clear(self):
        self.map = {}
        self.minx = sys.maxsize
        self.maxx = -sys.maxsize - 1
        self.miny = sys.maxsize
        self.maxy = -sys.maxsize - 1
        for overlay in self.overlays:
            overlay.clear()
    
    def top_right(self):
        return Coord2D(self.maxx, self.miny)

    def top_left(self):
        return Coord2D(self.minx, self.miny)

    def bottom_left(self):
        return Coord2D(self.minx, self.maxy)
    def bottom_right(self):
        return Coord2D(self.maxx, self.maxy)
    def corner(self, direction):
        if direction == NW:
            return self.top_left()
        if direction == NE:
            return self.top_right()
        if direction == SW:
            return self.bottom_left()
        if direction == SE:
            return self.bottom_right()
        
    def teleport(self, coord):
        return self.wormholes.get(coord, coord)
        

    def valid_neighbors(self, coord):
        for n in coord.neighbors():
            tn = self.teleport(n)
            val = self[tn]
            if val in self.invalid:
                continue

            yield((tn, val))
    
    def valid_surrounding(self, coord):
        for n in coord.surrounding_coords():
            tn = self.teleport(n)
            val = self[tn]
            if val in self.invalid:
                yield((tn, val))

    def create_wormhole(self, start, end, bidirectional=False):
        self.wormholes[start] = end
        if bidirectional:
            self.wormholes[end] = start


    def __iter__(self):
        return self.map.__iter__()
    
    def items(self):
        return self.map.items()

    def get_sub_map(self, point_a, point_b):
        top_left = Coord2D(min(point_a.x, point_b.x), min(point_a.y, point_b.y))
        bottom_right = Coord2D(max(point_a.x, point_b.x), max(point_a.y, point_b.y))
        new_map = Map2D(self.default)
        for coord in top_left.rectangle_tl_lr_coords(bottom_right):
            new_map[coord-top_left] = self[coord]
        return new_map

    def get_new_overlay(self, altitude):
        return Map2DOverlay(self, altitude)

    def add_overlay(self, altitude):

        new_overlay = self.get_new_overlay(altitude)
        self.overlays.append(new_overlay)
        self.overlays.sort(key=lambda x: x.altitude, reverse=True)
        return new_overlay

    def remove_overlay(self, overlay):
        del self.overlays[overlay]

    def _get_new_pointer_overlay(self):
        return PointerOverlay(self)

    def set_pointer(self, k, value):
        if not self.pointer_overlay:
            self.pointer_overlay = self._get_new_pointer_overlay()

        pointer = self.pointer_overlay
        pointer[k] = value

    def fill_from_lines(self, lines):
        y = 0
        for line in lines:
            x = 0
            for c in line:
                self[Coord2D(x, y)] = c
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
        self.map[k.copy()] = value

    def get(self, k, default):
        return self.map.get(k, default)

    def values(self):
        return self.map.values()
        
    def __delitem__(self, k):
        del self.map[k]

    def get_top(self, coord):
        if self.pointer_overlay:
            if coord in self.pointer_overlay:
                return self.pointer_overlay[coord]

        for overlay in self.overlays:
            if coord in overlay:
                return overlay[coord]
        return self[coord]

    def __hash__(self):
        return hash(frozenset(self.map.items()))

    def __len__(self):
        return len(self.map)

    def get_width(self):
        if self.perimeter_type == PerimeterType.RECTANGLE:
            return self.perimeter_maxx - self.perimeter_minx
        width = (self.maxx + 1) - self.minx
        if width < 0:
            return 0
        return width

    def get_height(self):
        if self.perimeter_type == PerimeterType.RECTANGLE:
            return self.perimeter_maxy - self.perimeter_miny
        height = (self.maxy + 1) - self.miny
        if height < 0:
            return 0
        return height

    def print(self, offset=0, max_y_size=1000, max_x_size=1000, default="."):

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
                coord = Coord2D(x, y)
                # if coord in self.map.keys():
                print(self.get_top(coord), end="")
                # else:
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

    def rectangle_coords(self, offset=0):
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
                yield Coord2D(x, y)

    def is_boundary(self, coord, offset=0):
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

    def count(self, value):
        return sum(1 for v in self.map.values() if v == value)
    
    def count_neighbors(self, coord, value):
        return sum(1 for n in coord.neighbor_coords() if self[n] == value)
    
    def count_surrounding(self, coord, value):
        return sum(1 for n in coord.surrounding_coords() if self[n] == value)

    def find(self, value):
        for k, v in self.map.items():
            if v == value:
                return k
        return None


def rectangle_coords(x, y, width, height):
    for y1 in range(y, y+height):
        for x1 in range(x, x+width):
            yield Coord2D(x1, y1)


def surrounding_coords(x, y):
    return [Coord2D(x + i.x, y + i.y) for i in SURROUNDING]


def neighbor_coords(x, y):
    return [Coord2D(x + i.x, y + i.y) for i in NEIGHBORS]


def build_min_distances(valid_coords):
    distances = {}
    for coord in valid_coords:
        distances[(coord, coord)] = 0
        for n in coord.neighbor_coords():
            if n in valid_coords:
                distances[(coord, n)] = 1

    for k in valid_coords:
        for i in valid_coords:
            for j in valid_coords:
                if (i, k) in distances:
                    dist_ik = distances[(i, k)]
                else:
                    continue
                if (k, j) in distances:
                    dist_kj = distances[(k, j)]
                else:
                    continue
                if (i, j) in distances:
                    dist_ij = min(distances[i, j], dist_ik + dist_kj)
                else:
                    dist_ij = dist_ik + dist_kj
                distances[(i, j)] = dist_ij
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


class InfiniteGrid(Map2D):
    def __init__(self, default_value):
        super().__init__(default_value)
