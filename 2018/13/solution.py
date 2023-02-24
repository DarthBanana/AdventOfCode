## advent of code 2018
## https://adventofcode.com/2018
## day 13
import copy
from Map2D import *

def TurnLeft(cart):    
    cart.heading_index =  ((len(NEIGHBORS) + cart.heading_index) - 1) % len(NEIGHBORS)
def TurnRight(cart):    
    cart.heading_index = (cart.heading_index + 1) % len(NEIGHBORS)
def Straight(cart):
    return
def Intersection(cart):
    INTERSECTION_ACTIONS[cart.next_intersection_index](cart)
    cart.next_intersection_index = (cart.next_intersection_index + 1) % len(INTERSECTION_ACTIONS)
def CurveA(cart):
    #/
    if NEIGHBORS[cart.heading_index] == W or NEIGHBORS[cart.heading_index] == E:
        TurnLeft(cart)
    else:
        TurnRight(cart)
def CurveB(cart):
    # \
    if NEIGHBORS[cart.heading_index] == W or NEIGHBORS[cart.heading_index] == E:
        TurnRight(cart)
    else:
        TurnLeft(cart)

TRACK_ACTIONS = {'-': Straight, '|': Straight, '\\': CurveB, '/': CurveA, '+': Intersection}


INTERSECTION_ACTIONS= [TurnLeft, Straight, TurnRight]

class Cart :
    def __init__(self, coord, heading):
        self.coord = coord
        self.heading_index = NEIGHBORS.index(heading)
        self.next_intersection_index = 0
        self.crashed = False
    
class Puzzle:
    def __init__(self, lines):
        self.map = InfiniteGrid()
        self.original_carts = []
        
        
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c == " ":
                    x += 1
                    continue
                coord = Coord2D(x,y)
                if c == "<":
                    self.original_carts.append(Cart(coord, W))                    
                    c = "-"
                elif c == ">":
                    self.original_carts.append(Cart(coord, E))                    
                    c = "-"
                elif c == "^":
                    self.original_carts.append(Cart(coord, N))                    
                    c = "|"
                elif c == "v":
                    self.original_carts.append(Cart(coord, S))                    
                    c = "|"
                self.map[coord] = c
                x += 1
            y += 1
        self.reset()
                   
    def reset(self):
        self.carts = copy.deepcopy(self.original_carts)
        self.cart_locations = {}
        self.crash_location = Coord2D(-1,-1)
        for cart in self.carts:
            self.cart_locations[cart.coord] = cart



    def run_step(self):
        self.carts.sort(key=lambda x:(x.coord.y, x.coord.x))                
        
        result = True        
        for cart in self.carts:           
             
            if cart.crashed:                                 
                continue
            old_location = cart.coord
            self.cart_locations.pop(old_location) 
            cart.coord = cart.coord + NEIGHBORS[cart.heading_index]                
                   
            if cart.coord in self.cart_locations:

                if (self.crash_location == Coord2D(-1,-1)):
                    self.crash_location = cart.coord
                cart.crashed = True
                self.cart_locations[cart.coord].crashed = True

                # CRASH
                print("CRASH", cart.coord)  
                self.cart_locations.pop(cart.coord)              
                result =  False
            else:
                self.cart_locations[cart.coord] = cart
            track = self.map[cart.coord]            
            TRACK_ACTIONS[track](cart)
        self.carts = list(filter(lambda x: x.crashed == False, self.carts))
        return result

    def part1(self):        
        self.map.print(default=" ")
        iteration = 0        
        print(iteration)
        while(self.run_step()):
            iteration+= 1
            print(iteration)            
            
            
        return "{},{}".format(self.crash_location.x, self.crash_location.y)

    def part2(self):
        self.reset()
        iteration = 0
        while(len(self.carts) > 1):

            print(iteration, len(self.carts))
            self.run_step()
            iteration += 1
        return "{},{}".format(self.carts[0].coord.x, self.carts[0].coord.y)