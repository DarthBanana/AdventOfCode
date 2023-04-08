## advent of code 2021
## https://adventofcode.com/2021
## day 03

from aocpuzzle import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.always_run_part_1 = True
        self.gamma_rate = ""
        self.epsilon = ""

    def count_ones_and_zeros(self, numbers, index):
        count0 = 0
        count1 = 0

        for e in numbers:
            if (e[index] == "1"):
                count1 += 1
            else:
                count0 += 1
        return count1, count0
    
    def part1(self):
        gamma_rate = ""
        epsilon=""
        for i in range(len(self.lines[0])):
            ones, zeros = self.count_ones_and_zeros(self.lines, i)
            
            if ones > zeros:
                gamma_rate += "1"
                epsilon += "0"
            else:
                gamma_rate += "0"
                epsilon += "1"
        self.epsilon = epsilon
        self.gamma_rate = gamma_rate
        epsilon = int(epsilon, 2)
        gamma_rate = int(gamma_rate, 2)
        return epsilon * gamma_rate

    def get_o2_generator_rating(self):
        candidates = self.lines
        index = 0
        while(len(candidates) > 1):            
            bit = "1"
            ones, zeros = self.count_ones_and_zeros(candidates, index)            
            if zeros > ones:
                bit = "0"
            new_candidates = []
            for c in candidates:
                if c[index] == bit:
                    new_candidates.append(c)
            candidates = new_candidates
            index += 1
        return int(candidates[0],2)

    def get_co2_scrubber_rating(self):
        candidates = self.lines
        index = 0
        while(len(candidates) > 1):
            bit = "0"
            ones, zeros = self.count_ones_and_zeros(candidates, index)
            if ones < zeros:
                bit = "1"
            new_candidates = []
            for c in candidates:
                if c[index] == bit:
                    new_candidates.append(c)
            candidates = new_candidates
            index += 1
        return int(candidates[0],2)

    def part2(self):
        o2_gen_rating = self.get_o2_generator_rating()
        co2_scrub_rating = self.get_co2_scrubber_rating()
        print(o2_gen_rating, co2_scrub_rating)
        return o2_gen_rating * co2_scrub_rating