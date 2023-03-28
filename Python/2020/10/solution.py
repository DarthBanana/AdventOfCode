## advent of code 2020
## https://adventofcode.com/2020
## day 10

from aocpuzzle import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.adapters = get_int_per_line(lines)
    def part1(self):
        sorted = self.adapters.copy()
        sorted.sort()
        sorted.append(sorted[-1] + 3)
        sorted.insert(0, 0)
        diffs = [sorted[i+1] - sorted[i] for i in range(len(sorted)-1)]
        return diffs.count(1) * diffs.count(3)        

    def part2(self):
        sorted = self.adapters.copy()
        sorted.sort()
        sorted.append(sorted[-1] + 3)
        sorted.insert(0, 0)
        options = [0 for i in range(len(sorted))]
        options[-1] = 1
        for i in range(len(sorted)-1, -1, -1):                       
            for j in range(i+1, len(sorted)):                
                if sorted[j] - sorted[i] > 3:
                    break
                options[i] += options[j]        
        return options[0]
                

