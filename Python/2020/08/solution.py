## advent of code 2020
## https://adventofcode.com/2020
## day 08

from aocpuzzle import *
from computer import *
class GameConsole(Computer):
    def __init__(self, lines):
        Computer.__init__(self)
        self.compile(lines)
        self.accumulator = 0

    def reset(self):
        super().reset()
        self.accumulator = 0
    def acc(self, x):
        self.accumulator += self.get_value(x)
        self.ip += 1

    def jmp(self, x):
        self.ip += self.get_value(x)

    def nop(self, x):
        self.ip += 1

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.console = GameConsole(lines)

    def part1(self):
        instructions = set()
        while(True):
            if self.console.ip in instructions:
                return self.console.accumulator
            instructions.add(self.console.ip)
            self.console.run(False, 1)

    def part2(self):

        for i in range(len(self.lines)):
            #print()
            #print(i)
            
            code = self.lines.copy()
            if code[i].startswith('jmp'):
                code[i] = code[i].replace('jmp', 'nop')
            elif code[i].startswith('nop'):
                code[i] = code[i].replace('nop', 'jmp')
            else:
                continue
            self.console.compile(code)
            self.console.reset()
            instructions = set()
            while(True):
                if self.console.ip in instructions:
                    break
                if self.console.ip >= len(code):
                    return self.console.accumulator
                instructions.add(self.console.ip)
                self.console.run(False, 1)


        