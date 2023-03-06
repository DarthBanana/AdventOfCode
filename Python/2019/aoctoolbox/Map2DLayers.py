from enum import Enum
import itertools
import sys
from Map2D import *

    
class InfiniteGridStack(InfiniteGrid):
    def __init__(self, default = 0):
        self.layers = []
        InfiniteGrid.__init__(self, default)

    def add_layer(self, layer):
        self.layers.insert(0, layer)
    
        
    def remove_layer(self, layer):
        self.layers.remove(layer)
    def __getitem__(self, k):
        for layer in self.layers:            
            if k in layer:                
                return layer[k]
        return InfiniteGrid.__getitem__(self, k)

