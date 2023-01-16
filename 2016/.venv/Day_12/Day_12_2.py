import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


class Computer:
    def __init__(self):

        self.registers = [0, 0, 0, 0]
        self.ip = 0

    def cpy(self, params):
        x, y = params
        self.registers[y] = x
        self.ip += 1

    def cpy_reg(self, params):
        x, y = params
        self.registers[y] = self.registers[x]
        self.ip += 1

    def inc(self, params):
        x = params
        val = self.registers[x]
        self.registers[x] += 1
        self.ip += 1

    def dec(self, params):
        x = params
        val = self.registers[x]
        self.registers[x] -= 1
        self.ip += 1
        if x == 3:
            print(self.registers[3])

    def jnz(self, params):
        x, y = params
        if not (x == 0):
            self.ip += y
        else:
            self.ip += 1

    def jnz_re(self, params):
        x, y = params

        self.jnz((self.registers[x], y))

    def compile_instruction(self, instruction_string):
        registers = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        cpy_reg_re = re.compile(r"cpy (\w) (\w)")
        cpy_int_re = re.compile(r"cpy (\d+) (\w)")
        inc_re = re.compile(r"inc (\w)")
        dec_re = re.compile(r"dec (\w)")
        jnz_re = re.compile(r"jnz (\w) (-*\d+)")
        jnz_int_re = re.compile(r"jnz (\d+) (-*\d+)")
        print(instruction_string)

        # print(self.ip, ": [a:", self.registers['a'], ", b:", self.registers['b'], ", c:", self.registers['c'], ", d:", self.registers['d'], "] - ", instruction_string)
        match = cpy_int_re.search(instruction_string)
        if (match):
            return (self.cpy, (int(match.group(1)), registers[match.group(2)]))

        match = cpy_reg_re.search(instruction_string)
        if (match):
            return (self.cpy_reg, (registers[match.group(1)], registers[match.group(2)]))

        match = inc_re.search(instruction_string)
        if (match):
            return (self.inc, (registers[match.group(1)]))

        match = dec_re.search(instruction_string)
        if (match):
            return (self.dec, (registers[match.group(1)]))

        match = jnz_int_re.search(instruction_string)
        if (match):
            return (self.jnz, (int(match.group(1)), int(match.group(2))))

        match = jnz_re.search(instruction_string)
        if (match):
            return (self.jnz_re, (registers[match.group(1)], int(match.group(2))))

    def compile_instructions(self, program):
        instructions = []
        for line in program.splitlines():
            instructions.append(self.compile_instruction(line))
        return instructions

    def execute_instruction(self, instruction):
        # print(instruction)
        func, params = instruction
        func(params)
        # print(self.registers)

    def execute_program(self, program):
        instructions = self.compile_instructions(program)

        while 0 <= self.ip < len(instructions):
            self.execute_instruction(instructions[self.ip])


test_program = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


real_program = """\
cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 19 c
cpy 11 d
inc a
dec d
jnz d -2
dec c
jnz c -5"""

real_program_2 = """\
cpy 1 c
cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 19 c
cpy 11 d
inc a
dec d
jnz d -2
dec c
jnz c -5"""


def test():
    computer = Computer()
    computer.execute_program(test_program)
    print(computer.registers)
    return computer.registers[0]


def run():
    computer = Computer()
    computer.execute_program(real_program)
    print(computer.registers[0])


def run_part2():
    computer = Computer()
    computer.execute_program(real_program_2)
    print(computer.registers[0])


assert (test() == 42)
run_part2()
