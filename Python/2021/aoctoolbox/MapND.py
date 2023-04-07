from CoordND import *
class MapND:
    def __init__(self, default=None):
        self.default = default
        self.invalid = set("#")
        self.clear()

    def refresh(self):
        pass

    def clear(self):
        self.map = {}
        self.mins = None
        self.maxs = None
    
    def valid_neighbors(self, coord):
        for n in coord.neighbors():            
            val = self[n]
            if val in self.invalid:
                continue

            yield((n, val))
    
    def valid_surrounding(self, coord):
        for n in coord.surrounding_coords():            
            val = self[n]
            if val in self.invalid:
                yield((n, val))


    def __iter__(self):
        return self.map.__iter__()
    
    def items(self):
        return self.map.items()


    def __getitem__(self, k):

        return self.map.get(k, self.default)

    def __setitem__(self, k, value):

        self.mins = k.min(self.mins)
        self.maxs = k.max(self.maxs)
        self.map[k.copy()] = value


    def __hash__(self):
        return hash(frozenset(self.map.items()))

    def __len__(self):
        return len(self.map)

    def get_dimensions(self):
        dims = CoordND(tuple(lambda min, max: (max + 1) - min, self.min, self.max))
        return dims

    def print_plane(self, z, offset=0, default="."):
        print()
        print("z = ", z)
        y_range = range(self.mins[1] - offset, self.maxs[1] + 1 + offset)
        x_range = range(self.mins[0] - offset, self.maxs[0] + 1 + offset)
        for y in y_range:            
            for x in x_range:
                coord = CoordND((x, y, z))
                if coord in self.map.keys():
                    print(self[coord], end="")
                else:
                    print(default, end="")
            print()
    
    def print3d(self, offset=0, max_y_size=1000, max_x_size=1000, default="."):
        if len(self.mins) != 3:
            print("Only support 3 dimensions many dimensions")
            return       

        print()
        z_range = range(self.mins[2] - offset, self.maxs[2] + 1 + offset)
        for z in z_range:
            self.print_plane(z, offset, default)
            
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