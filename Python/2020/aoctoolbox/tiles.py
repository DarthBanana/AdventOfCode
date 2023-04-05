##
## Some kind of utility for working with tiles
## of fixed dimensions.  Relies on the numpy.
## supports glueing tiles together, and
## folding them in 3d space
## 
## This would be useful for AOC 2022 day 22
## and 2020 day 20
##
import numpy as np
class Tile:
    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.data = np.zeros((x_dim, y_dim), dtype=np.int)
        self.x = 0
        self.y = 0
        self.z = 0
        self.x_flip = False
        self.y_flip = False
        self.z_flip = False
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return str(self.data)
    def __eq__(self, other):
        return self.data == other.data
    def __ne__(self, other):
        return self.data != other.data
    def __hash__(self):
        return hash(self.data)
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
        
        