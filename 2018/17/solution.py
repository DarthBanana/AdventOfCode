## advent of code 2018
## https://adventofcode.com/2018
## day 17

import re
from Map2DLayers import *

line_re = re.compile(r"(\w)=(\d+), (\w)=(\d+)..(\d+)")
class Puzzle:
    def __init__(self, lines):
        self.map = InfiniteGridStack(".")
        self.water_map = {}
        self.drip_map = {}
        self.map.add_layer(self.water_map)
        self.map.add_layer(self.drip_map)

        for line in lines:
            match = line_re.search(line)
            if match.group(1) == "x":
                x = int(match.group(2))
                y_range = range(int(match.group(4)), int(match.group(5))+1)
                for y in y_range:
                    self.map[Coord2D(x,y)] = "#"                
            else:
                x_range = range(int(match.group(4)), int(match.group(5))+1)
                y = int(match.group(2))
                for x in x_range:
                    self.map[Coord2D(x,y)] = "#"
        self.water_source = Coord2D(500,self.map.miny)
        self.water_map[Coord2D(500,0)] = "+"        
        self.map.set_rectangle_perimeter(0, 0, self.map.miny-1, 100000000, self.map.maxy+1)    
        #self.map.set_auto_rectangle_perimeter(0)
        self.reset()
        self.map.print(offset=1)
    
    def reset(self):
        self.settled = False
        self.drip_map.clear()
        self.overflow = False
        self.water_map.clear()

    def flow(self, coord, direction):    
        
        cur = coord
        while not self.map[coord] == "#":
            self.drip_map[coord] = "|"
            if self.map[coord + DOWN] == ".":
                self.drip_down(coord)
        
                return False
            coord = coord + direction
        
        return True
        if not self.map[coord] == ".":
            return True
        self.drip_map[coord] = "|"
        if self.map[coord + DOWN]:
            self.drip_down(coord)
            return False
        else:
            blocked = self.flow(coord + direction, direction)
            if blocked:
                self.water_map[coord] = "~"
                self.drip_map.pop(coord)
                return True
            return False

    def settle(self, coord): 
        self.settled = True       
        
        cur = coord
        while not self.map[coord + LEFT] == "#":
            coord = coord + LEFT

        while not self.map[coord] == "#":
            self.drip_map.pop(coord)
            self.water_map[coord] = "~"   
            coord = coord + RIGHT     
        
        
    def drip_down(self, coord):
        
        # Try to go down as far as possible
        self.drip_map[coord] = "|"        
        while(True):
            next = coord + DOWN
            next_tile = self.map[next]
            
            if next_tile == 0:
                # went off the map
                self.overflow = True
                return
            elif next_tile == "|":
                return
            elif not next_tile == ".":
                break
            self.drip_map[next] = "|"
            coord = next
        left_blocked = self.flow(coord+LEFT, LEFT)
        right_blocked = self.flow(coord+RIGHT, RIGHT)
        if left_blocked and right_blocked:
            self.settle(coord)
        return 

    def drip(self, coord):
        
        self.drip_map.clear()
        self.drip_down(coord)        

    def fill_er_up(self):
        still_going = True
        self.settled = True
        while self.settled == True:
            self.settled = False            
            self.drip(self.water_source)
        return

    def count_overflow(self):
        count = 0


    def part1(self):
        self.fill_er_up()
        self.map.print(offset=1)
        #print(self.water_map)
        #print(self.drip_map)
        return len(self.water_map) + len(self.drip_map)
        

    def part2(self):
        return len(self.water_map)
        