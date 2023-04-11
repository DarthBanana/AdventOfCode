## advent of code 2021
## https://adventofcode.com/2021
## day 14

from aocpuzzle import *
import itertools
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.start = lines[0]
        self.insertions = {}
        for line in lines[2:]:
            split = line.split(" -> ")
            self.insertions[split[0]] = (split[1], split[0][0] + split[1], split[1] + split[0][1])
        self.pair_counts = {}
        for ab in itertools.pairwise(self.start):
            ab = "".join(ab)
            self.pair_counts[ab] = self.pair_counts.get(ab, 0) + 1
        self.letter_counts = {}

        for c in self.start:
            self.letter_counts[c] = self.letter_counts.get(c, 0) + 1
    
    def run_counts(self, iterations):
        pair_counts = self.pair_counts.copy()
        letter_counts = self.letter_counts.copy()

        for i in range(iterations):
            new_pairs = {}
            for pair, c in pair_counts.copy().items():
                ltr, left, right = self.insertions[pair]                
                letter_counts[ltr] = letter_counts.get(ltr, 0) + c
                new_pairs[left] = new_pairs.get(left, 0) + c
                new_pairs[right] = new_pairs.get(right, 0) + c
            pair_counts = new_pairs        
        values = letter_counts.values()
        return max(values) - min(values)
        
    def part1(self):
        return self.run_counts(10)

    def part2(self):        
        return self.run_counts(40)