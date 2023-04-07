## advent of code 2020
## https://adventofcode.com/2020
## day 23

from aocpuzzle import *
import numpy as np

def labels(next_cups, count, start=0):
    if count:
        yield next_cups[start]+1
        yield from labels(next_cups, count-1, next_cups[start])

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.initialize_ring()
                
    def initialize_ring(self, max_value = 0):
        cups = np.array([int(r)-1 for r in self.lines[0]])
        cups = np.r_[cups, np.mgrid[len(cups):max_value]]
        self.next_cups = np.zeros_like(cups)
        self.next_cups[cups] = np.roll(cups, -1)
        self.current = cups[0]
        self.max_cup = len(self.next_cups)
    
    def make_move(self):
        next = self.next_cups
        cur = self.current
        cup1 = next[cur]
        cup2 = next[cup1]
        cup3 = next[cup2]
        dest = cur
        while (dest:=dest-1)%len(next) in (cup1, cup2, cup3): pass
        #while (True):
        #    dest = (dest-1)%self.max_cup
        #    if dest not in (cup1, cup2, cup3):
        #        break
        next[cur] = next[cup3]
        next[cup3] = next[dest]
        next[dest] = cup1
        self.current = next[cur]         
        

    def part1(self):                
        print(self.next_cups)
        for i in range(100):            
            self.make_move()
        return "".join(map(str, labels(self.next_cups, len(self.next_cups)-1)))
    def part2(self):

        self.initialize_ring(10**6)
        for i in range(10**7):
            self.make_move()
        next_two = list(labels(self.next_cups, 2))
        print(next_two)
        return np.prod(next_two, dtype=np.int64)
        