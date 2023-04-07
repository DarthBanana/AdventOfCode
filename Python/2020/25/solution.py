## advent of code 2020
## https://adventofcode.com/2020
## day 25

from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.card_public_key = int(lines[0])
        self.door_public_key = int(lines[1])

    def transform_iteration(self, value, subject_number):
        return (value * subject_number) % 20201227
        
    def transform(self, subject_number, loop_size):
        val = 1
        for i in range(loop_size):
            val = self.transform_iteration(val, subject_number)            
        return val

    def derive_loop_size(self, public_key):
        val = 1
        count = 0
        while(val != public_key):
            val = self.transform_iteration(val, 7)
            count += 1
        return count

    def part1(self):
        #door_loop_size = self.derive_loop_size(self.door_public_key)
        card_loop_size = self.derive_loop_size(self.card_public_key)
        #encryption_key=self.transform(self.card_public_key, door_loop_size)
        encryption_key2=self.transform(self.door_public_key, card_loop_size)
        #print(door_loop_size, card_loop_size)
        return encryption_key2

    def part2(self):
        pass