## advent of code 2018
## https://adventofcode.com/2018
## day 05
from functools import reduce

def is_match(x,y):
    if len(x) == 0:
        return False
    
    return (abs(ord(x[len(x)-1]) - ord(y)) == 32)

def react(string):
    return reduce((lambda x,y: x[:-1] if is_match(x, y) else x + y), string)

class Puzzle:
    def __init__(self, lines):
        self.input = lines[0].strip()
        self.chars = set()
        for c in self.input:
            self.chars.add(c.lower())


    def part1(self):
        output = react(self.input)        
        return len(output)
        

    def part2(self):
        shortest = len(self.input)
        for c in self.chars:
            input = self.input
            input = input.replace(c, '').replace(c.upper(), '')
            output = react(input)
            shortest = min(shortest, len(output))
        return shortest