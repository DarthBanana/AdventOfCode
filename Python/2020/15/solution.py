## advent of code 2020
## https://adventofcode.com/2020
## day 15

from aocpuzzle import *
from parsehelp import *
import numpy as np

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.starting_nums = get_all_ints(lines[0])

    def play_n_turns(self, n):        
        history = {}
        last_spoken = None
        spoken = None        
        
        for t in range(n):
            if t < len(self.starting_nums):
                spoken = self.starting_nums[t]
            else:                
                if last_spoken in history:
                    spoken = (t-1) - history[last_spoken]
                else:
                    spoken = 0
        
            if last_spoken is not None:
                history[last_spoken] = t-1
                                
            last_spoken = spoken
        
        return last_spoken    


    def play_n_turns2(self, n):        
        history = {}
        last_spoken = None
        spoken = None        
        t = 0
        history = np.full(n, -1, dtype=np.int64)
        for t in range(n):
            if t < len(self.starting_nums):
                spoken = self.starting_nums[t]
            else:                
                if history[last_spoken] == -1:
                    spoken = 0
                else:
                    spoken = (t-1) - history[last_spoken]
                                
        
            if last_spoken is not None:
                history[last_spoken] = t-1
                
                        
            last_spoken = spoken

        return last_spoken
                    
    def part1(self):
        return self.play_n_turns(2020)

    def part2(self):         
        return self.play_n_turns(30000000)