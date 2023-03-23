## advent of code 2019
## https://adventofcode.com/2019
## day 11

import os
from aocpuzzle import *
from intcode import *
from parsehelp import *
from Map2D import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        
        self.computer = MyIntcodeComputer()        

        self.computer.load_program_from_input(lines)
        #self.computer.interpret_program()        
        #assert(False)
        
        AoCPuzzle.__init__(self, lines, is_test)
        
        self.reset()
        
    def reset(self):
        self.map = Map2D(' ')       
        self.robot_map = self.map.add_overlay(1)
        
        self.computer.reset()
        self.robot_location = Coord2D(0,0)
        self.robot_direction = Direction(UP)

    def part1(self):
        count = 0
        input_mailbox = self.computer.rx_mailbox
        output_mailbox = self.computer.tx_mailbox
        while(self.computer.can_continue()):
            current_color = self.map[self.robot_location]
            if current_color == '.' or current_color == ' ':                
                input_mailbox.send(0)
            else:
                input_mailbox.send(1)
            
            self.computer.run()
            

            assert(len(output_mailbox) == 2)
            #print(output_mailbox.mailbox)
            color = output_mailbox.receive()
            turn = output_mailbox.receive()
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