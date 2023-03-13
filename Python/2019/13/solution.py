## advent of code 2019
## https://adventofcode.com/2019
## day 13

import os
from time import sleep
from aocpuzzle import *
from intcode import *
from PrettyMap2D import *
from parsehelp import get_all_ints

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.code = get_all_ints(lines[0])
        self.input_mailbox = Mailbox()
        self.output_mailbox = Mailbox()

        self.computer = MyIntcodeComputer(self.input_mailbox, self.output_mailbox)
        self.computer.load_program(self.code)
        self.reset()

    def reset(self):
        self.score = 0
        self.input_mailbox.reset()
        self.output_mailbox.reset()
        self.computer.reset()
        
        self.map = PrettyInfiniteGrid()

    def run_program(self):
        self.computer.run()
    
    
        assert(len(self.output_mailbox) % 3 == 0)
        while(len(self.output_mailbox) > 0):
            x = self.output_mailbox.receive()
            y = self.output_mailbox.receive()
            tile = self.output_mailbox.receive()
            if tile == 0:
                tile = ' '
            elif tile == 1:
                tile = '#'
            elif tile == 2:
                tile = 'X'
            elif tile == 3:
                tile = '-'
            elif tile == 4:
                tile = 'o'
            else:
                assert(False)
            self.map[Coord2D(x,y)] = tile

    def play_game(self):
        self.computer[0] = 2
        
        paddle_x = 0
        ball_x = 0
        while(self.computer.can_continue()):
            self.computer.run()
            assert(len(self.output_mailbox) % 3 == 0)
            while(len(self.output_mailbox) > 0):
                x = self.output_mailbox.receive()
                y = self.output_mailbox.receive()
                tile = self.output_mailbox.receive()
                if x == -1 and y == 0:
                    self.score = tile
                else:
                    if tile == 0:
                        tile = ' '
                    elif tile == 1:
                        tile = '#'
                    elif tile == 2:
                        tile = 'X'
                    elif tile == 3:
                        tile = '-'
                        paddle_x = x
                    elif tile == 4:
                        tile = 'o'
                        ball_x = x
                    else:
                        assert(False)
                    self.map[Coord2D(x,y)] = tile
            #os.system('CLS')
            #print(self.score)
            #self.map.print()
            #sleep(0.01)

            
            if ball_x < paddle_x:
                self.input_mailbox.send(-1)
            elif ball_x > paddle_x:
                self.input_mailbox.send(1)
            else:
                self.input_mailbox.send(0)


            
    def part1(self):
        self.run_program()
        #self.map.print()
        return self.map.count('X')

    def part2(self):
        self.reset()
        self.play_game()
        return self.score