## advent of code 2019
## https://adventofcode.com/2019
## day 02
from aocpuzzle import *
from computer import *
from parsehelp import *
class MyIntcodeComputer(IntcodeComputer):
    def __init__(self):
        IntcodeComputer.__init__(self)
        self.instmap = {1:(self.add, 3), 2:(self.mul, 3), 99:(self.halt, 0)}
        self.set_instruction_set(self.instmap)

    def add(self, x, y, z):
        self[z] = x + y
        self.ip += 4
    def mul(self, x, y, z):
        self[z] = x * y  
        self.ip += 4
    def halt(self):
        self.ip = -1



class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test = False):
        AoCPuzzle.__init__(self, lines)
        self.code = get_all_ints(lines[0])

    def part1(self):
        computer = MyIntcodeComputer()
        code = self.code.copy()
        if self.is_test:
            target_instruction = code.pop(0)
        else:            
            target_instruction = 0
            code[1] = 12
            code[2] = 2        
        computer.load_program(code)
        computer.run(True)
        return computer[target_instruction]

    def part2(self):       
        
        computer = MyIntcodeComputer()
        code = self.code.copy()        
        computer.load_program(code)
        for noun in range(0, 100):
            for verb in range(0, 100):
                computer.reset()
                computer[1] = noun
                computer[2] = verb
                computer.run()
                if computer[0] == 19690720:
                    return 100 * noun + verb
                