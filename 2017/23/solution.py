## advent of code 2017
## https://adventofcode.com/2017
## day 23
from collections import deque
import sympy
import re

PART_ONE = False


class Puzzle:
    def __init__(self, lines):
        self.compile(lines)
        self.reset()

    def reset(self):
        self.register_values = {}
        self.ip = 0
        self.mul_count = 0
        for reg in self.register_names:
            self.register_values[reg] = 0

    def compile_line(self, line):
        parts = line.split()
        cmd = parts[0]
        params = []
        for i in range(1, len(parts)):
            param = parts[i]
            if param.isalpha():
                self.register_names.add(param)
                params.append(param)
            else:
                params.append(int(param))

        if cmd == "snd":
            command = self.snd
        elif cmd == "set":
            command = self.set
        elif cmd == "add":
            command = self.add
        elif cmd == "mul":
            command = self.mul
        elif cmd == "mod":
            command = self.mod
        elif cmd == "rcv":
            command = self.rcv
        elif cmd == "jgz":
            command = self.jgz
        elif cmd == "jnz":
            command = self.jnz
        elif cmd == "sub":
            command = self.sub
        else:
            assert False

        return (cmd, command, params)

    def compile(self, lines):
        self.register_names = set()
        self.instructions = []
        for line in lines:
            self.instructions.append(self.compile_line(line))

    def get_value(self, value):
        if not (type(value) == int):
            value = self.register_values[value]
        return value

    def crack_two_params(self, param):
        target, value = param
        value = self.get_value(value)
        return target, value

    def snd(self, param):
        value = self.get_value(param[0])
        self.send_pipe.send(value)
        self.ip += 1

    def set(self, param):
        target, value = param
        value = self.get_value(value)

        self.register_values[target] = value
        self.ip += 1

    def add(self, param):
        target, value = self.crack_two_params(param)
        self.register_values[target] += value
        self.ip += 1

    def sub(self, param):
        target, value = self.crack_two_params(param)
        self.register_values[target] -= value
        self.ip += 1

    def mul(self, param):
        target, value = self.crack_two_params(param)
        self.register_values[target] *= value
        self.ip += 1
        self.mul_count += 1

    def mod(self, param):
        target, value = self.crack_two_params(param)
        self.register_values[target] %= value
        self.ip += 1

    def rcv(self, param):
        value = self.get_value(param[0])
        if PART_ONE:
            if value == 0:
                self.ip += 1
            else:
                self.recovered_frequency = self.receive_pipe.receive()
                print(self.recovered_frequency)
                self.ip = -1
        else:
            if self.receive_pipe.is_empty():
                self.waiting = True
            else:
                value = param[0]
                result = self.receive_pipe.receive()
                self.waiting = False
                self.register_values[value] = result

                self.ip += 1

    def jgz(self, param):
        offset = self.get_value(param[1])
        cmp = self.get_value(param[0])
        if cmp > 0:
            self.ip += offset
        else:
            self.ip += 1

    def jnz(self, param):
        offset = self.get_value(param[1])
        cmp = self.get_value(param[0])
        if cmp == 0:
            self.ip += 1
        else:
            self.ip += offset

    def print_instruction(self, instruction):
        cmd = instruction[0]
        print(self.id, " --- ", self.ip, ": ", cmd, end=" ")
        for param in instruction[2]:
            print(param, end=" ")
        print()

    def execute(self):

        while 0 <= self.ip < len(self.instructions):
            instruction = self.instructions[self.ip]
            instruction[1](instruction[2])
        return


def parse_input(lines):
    return Puzzle(lines)


def part1(puzzle):
    puzzle.reset()
    puzzle.execute()
    return puzzle.mul_count


def part2(data):
    result = 0
    for num in range(108400, 125400 + 1, 17):
        if not sympy.isprime(num):
            result += 1
    return result
