## advent of code 2019
## https://adventofcode.com/2019
## day 11

import os
from aocpuzzle import *
from intcode import *
from parsehelp import *
from Map2DLayers import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        self.input_mailbox = Mailbox(False)
        self.output_mailbox = Mailbox(False)
        self.computer = MyIntcodeComputer(self.input_mailbox, self.output_mailbox)
        self.code = get_all_ints(lines[0])

        self.computer.load_program(self.code)
        #self.computer.interpret_program()        
        
        AoCPuzzle.__init__(self, lines, is_test)
        
        self.reset()
        
    def reset(self):
        self.map = InfiniteGridStack(' ')       
        self.robot_map = {}
        #self.map.add_layer(self.robot_map) 
        self.computer.reset()
        self.robot_location = Coord2D(0,0)
        self.robot_direction = Direction(UP)

    def part1(self):
        count = 0
        while(self.computer.can_continue()):
            current_color = self.map[self.robot_location]
            if current_color == '.' or current_color == ' ':                
                self.input_mailbox.send(0)
            else:
                self.input_mailbox.send(1)
            
            self.computer.run()
            

            assert(len(self.output_mailbox) == 2)
            #print(self.output_mailbox.mailbox)
            color = self.output_mailbox.receive()
            turn = self.output_mailbox.receive()
            if color == 0:
                self.map[self.robot_location] = '.'
            else:
                assert(color == 1)
                self.map[self.robot_location] = '#'
            
            if turn == 0:
                self.robot_direction.turn_left_90()
            else:
                assert(turn == 1)
                self.robot_direction.turn_right_90()
            
            self.robot_location += self.robot_direction
            
            #os.system('CLS')
            #self.map.print(offset=3)
            
            count += 1
        self.map.print(offset=3)
        
        return len(self.map)

    def part2(self):
        self.reset()
        self.map[self.robot_location] = '#'
        self.part1()
        self.map.print()
        return "HAFULAPE"