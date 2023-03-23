## advent of code 2019
## https://adventofcode.com/2019
## day 08

from aocpuzzle import *
from Map2D import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test=False)
        line = lines[0]
        if is_test:
            self.width = 2
            self.height = 2
        else:
            self.width = 25
            self.height = 6

        self.layers = []
        self.pixels = []

        for c in line:
            self.pixels.append(int(c))

        assert(len(self.pixels) % (self.width * self.height) == 0)
        self.num_layers = len(self.pixels) // (self.width * self.height)
        for i in range(self.num_layers):
            layer = self.pixels[i * self.width * self.height : (i+1) * self.width * self.height]
            self.layers.append(layer)

    def part1(self):
        min_zeroes = 1000000
        min_layer = None

        for layer in self.layers:
            zeroes = layer.count(0)
            if zeroes < min_zeroes:
                min_zeroes = zeroes
                min_layer = layer
        return min_layer.count(1) * min_layer.count(2)


    def part2(self):
        map = Map2D('.')
        map.minx = -1
        map.maxx = self.width+1
        map.miny = -1
        map.maxy = self.height+1
        #map[Coord2D(0,0)] = 'X'
        layer_maps = []
        for i in range(self.num_layers):
            new_map = map.add_overlay(i + 1)
            layer_maps.insert(0,new_map)             
        #layer_maps.reverse
        for i in range(self.num_layers):
            layer = self.layers[i]
            layer_map = layer_maps[i]

            for y in range(self.height):
                for x in range(self.width):
                    value = layer[y * self.width + x]
                    if value == 0:
                        layer_map[Coord2D(x,y)] = ' '
                    elif value == 1:                        
                        layer_map[Coord2D(x,y)] = '#'
                    else:
                        continue

            
        print("OUTPUT:")
        map.print()
        return "YEHEF"

