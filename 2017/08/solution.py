## advent of code 2017
## https://adventofcode.com/2017
## day 08

import re

instruction_re = re.compile(
    r"(\w+) (inc|dec) (-?\d*) if (\w+) (>|<|>=|==|<=|!=) (-?\d*)"
)


class Instruction:
    def __init__(self, line):
        self.register_names = set()
        match = instruction_re.search(line)
        self.target_reg = match.group(1)
        if match.group(2) == "inc":
            self.multiplier = 1
        else:
            self.multiplier = -1

        self.modifier = int(match.group(3))
        self.comp_reg = match.group(4)
        self.comparison = match.group(5)
        self.comparitor = int(match.group(6))


class Puzzle:
    def __init__(self, lines):
        self.instructions = []
        self.register_names = set()
        for line in lines:
            instruction = Instruction(line)
            self.instructions.append(instruction)
            self.register_names.add(instruction.target_reg)
            self.register_names.add(instruction.comp_reg)

    def reset_registers(self):
        self.highest_reg_value = 0
        self.registers = {}
        for reg in self.register_names:
            self.registers[reg] = 0

    def execute_instruction(self, instruction):
        value1 = self.registers[instruction.comp_reg]
        value2 = instruction.comparitor
        should_execute = False
        if instruction.comparison == "==":
            should_execute = value1 == value2
        elif instruction.comparison == "!=":
            should_execute = not (value1 == value2)
        elif instruction.comparison == ">":
            should_execute = value1 > value2
        elif instruction.comparison == "<":
            should_execute = value1 < value2
        elif instruction.comparison == "<=":
            should_execute = value1 <= value2
        elif instruction.comparison == ">=":
            should_execute = value1 >= value2
        else:
            assert False
        if should_execute:
            old_value = self.registers[instruction.target_reg]
            new_value = old_value + instruction.modifier * instruction.multiplier
            self.highest_reg_value = max(self.highest_reg_value, new_value)
            self.registers[instruction.target_reg] = new_value

    def run_program(self):
        for instruction in self.instructions:
            self.execute_instruction(instruction)

    def get_largest_register_value(self):
        max_value = 0
        for reg in self.registers.values():
            max_value = max(max_value, reg)

        return max_value


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.reset_registers()
    puzzle.run_program()
    return puzzle.get_largest_register_value()


def part2(puzzle):
    return puzzle.highest_reg_value
