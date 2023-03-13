## advent of code 2019
## https://adventofcode.com/2019
## day 15

import random
from time import sleep
from aocpuzzle import *
from intcode import *
from parsehelp import *
from PrettyMap2D import *
import networkx as nx
import matplotlib.pyplot as plt

DIRECTION_TRANSLATOR = {N: (1,'^'), S: (2,'v'), W: (3,'<'), E: (4,'>')}
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.code = get_all_ints(lines[0])
        self.map = PrettyInfiniteGrid()
        
        self.input_mailbox = Mailbox(False)
        self.output_mailbox = Mailbox(False)
        self.computer = MyIntcodeComputer(self.input_mailbox, self.output_mailbox)
        self.computer.load_program(self.code)
        self.reset()
        self.droid_position = Coord2D(0,0)
        self.droid_direction = N
        self.destination = None
        self.graph = nx.Graph()
        self.interested = []
        self.walls = set()

    def reset(self):     
        
        self.computer.reset()
        self.input_mailbox.reset()
        self.output_mailbox.reset()
    
    def process_output(self):
        output = self.output_mailbox.receive()
        if output == 0:
            self.map[self.droid_position + self.droid_direction] = '#'
            self.walls.add(self.droid_position + self.droid_direction)
            self.graph.remove_node(self.droid_position + self.droid_direction)            
        elif output == 1:
            self.map[self.droid_position] = '.'
            self.droid_position = self.droid_position + self.droid_direction
            
        elif output == 2:
            self.droid_position = self.droid_position + self.droid_direction
            self.map[self.droid_position] = 'O'
            self.destination = self.droid_position
        else:
            raise Exception("Invalid output: " + str(output))
        if self.destination is not None:
            self.map[self.destination] = 'X'
        
        

    def part1(self):
        
        
        #self.map.autodraw = False
        self.visited = set()
        self.interested = []
        self.graph.add_node(self.droid_position)        
        current_interested = None
        current_path = []
        self.map[self.droid_position] = '.'
        while self.computer.can_continue():
            if self.droid_position in self.interested:
                self.interested.remove(self.droid_position)
            
            if self.droid_position not in self.visited:
                self.visited.add(self.droid_position)
                for position in self.droid_position.neighbor_coords():                    
                    if position not in self.visited:          
                        if position not in self.interested:              
                            self.interested.append(position)
                        self.graph.add_edge(self.droid_position, position)
                    else:
                        if self.map[position] != '#':
                            self.graph.add_edge(self.droid_position, position)
            if current_interested:
                if current_interested == self.droid_position:
                    assert(len(current_path)== 0)
                    current_interested = None
            if not current_interested:
                if len(self.interested) == 0:
                    break

                self.interested.sort(key=lambda x: self.droid_position.distance(x))
                
                current_interested = self.interested[0]
                #print("Current, target = ", self.droid_position, current_interested)
                assert(current_interested not in self.visited)
                assert(current_interested not in self.walls)
                assert(self.map[current_interested] != '#')
                
                self.current_path = nx.astar_path(self.graph, self.droid_position, current_interested)
                #print("New Path: ", self.current_path)
                next_position = self.current_path.pop(0)
            assert(len(self.current_path) > 0)
            next_position = self.current_path.pop(0)
            assert(next_position != self.droid_position)
            self.droid_direction = next_position - self.droid_position
            assert(next_position not in self.walls)                       

            self.map.set_pointer(self.droid_position, DIRECTION_TRANSLATOR[self.droid_direction][1])
            #self.map[self.droid_position] = DIRECTION_TRANSLATOR[self.droid_direction][1]                
            assert(self.droid_direction)
            assert(self.droid_direction in DIRECTION_TRANSLATOR)
            self.input_mailbox.send(DIRECTION_TRANSLATOR[self.droid_direction][0])
            #print("Current position, direction = ", self.droid_position, self.droid_direction)
            #self.map.print()
            self.computer.run()

            self.process_output()
            if self.droid_position != next_position:
                #print("Must have hit a wall??")
                assert(self.map[next_position] == '#')
                self.current_path = []
                current_interested = None
                if next_position in self.interested:
                    self.interested.remove(next_position)
                self.visited.add(next_position)

            self.map.set_pointer(self.droid_position, DIRECTION_TRANSLATOR[self.droid_direction][1])
        target = self.map.find('X')    
        length = nx.shortest_path_length(self.graph, Coord2D(0,0), target)
        print(length)
        return length
    def part2(self):
        self.map.autodraw = True
        self.map[Coord2D(0,0)] = '.'
        self.map.refresh()
        
        start = self.map.find('X')
        water = self.map.add_overlay(4)
        time = 0        
        self.filled = set()
        next_round = [start]
        while len(next_round) > 0:
            print(time)
            current_round = next_round
            next_round = []
            for position in current_round:
                self.filled.add(position)
                water[position] = 'O'
                #self.map[position] = 'O'
                for neighbor in position.neighbor_coords():
                    #print(self.map.get_top(neighbor))
                    if(self.map.get_top(neighbor) == '.'):
                        next_round.append(neighbor)
                    
            time += 1
            sleep(0.01)
        #assert(self.map.count('.') ==)
        print(time-1)
        return time-1

