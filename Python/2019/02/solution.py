## advent of code 2019
## https://adventofcode.com/2019
## day 02
from aocpuzzle import *
from intcode import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test = False):
        AoCPuzzle.__init__(self, lines, is_test)
        self.computer = MyIntcodeComputer()        
        self.code = get_all_ints(lines[0])

    def part1(self):        
        code = self.code.copy()
        if self.is_test:
            target_instruction = code.pop(0)
        else:            
            target_instruction = 0
            code[1] = 12
            code[2] = 2        
        self.computer.load_program(code)
        self.computer.reset()
        self.computer.run(True)
        return self.computer[target_instruction]

    def part2(self):       
                
        code = self.code.copy()        
        self.computer.load_program(code)
        for noun in range(0, 100):
            for verb in range(0, 100):
                self.computer.reset()
                self.computer[1] = noun
                self.computer[2] = verb
                self.computer.run()
                if self.computer[0] == 19690720:
                    return 100 * noun + verb
                