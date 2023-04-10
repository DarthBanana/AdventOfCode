## advent of code 2021
## https://adventofcode.com/2021
## day 06

from aocpuzzle import *
from parsehelp import *
class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.fish = get_all_ints(lines[0])

        self.counts = {}
        for i in range(9):
            self.counts[i] = self.fish.count(i)
    
    def calculate_fish(self, days):
        current_state = self.counts.copy()
        for i in range(days):
            new_state = {
                0: current_state[1],
                1: current_state[2],
                2: current_state[3],
                3: current_state[4],
                4: current_state[5],
                5: current_state[6],
                6: current_state[7] + current_state[0],
                7: current_state[8],
                8: current_state[0]
            }
            current_state = new_state
        return sum(current_state.values())
    
    def simulate(self, days):
        fish = self.fish.copy()
        print(fish)
        for i in range(days):
            new_fish = []
            for i in range(len(fish)):
                timer = fish[i]
                if timer == 0:
                    new_fish.append(8)
                    new_fish.append(6)                    
                else:
                    new_fish.append(timer - 1)
            fish = new_fish
                    
        return len(fish)

    def part1(self):
        count = self.calculate_fish(80)
        return count

    def part2(self):
        
        return self.calculate_fish(256)