## advent of code 2017
## https://adventofcode.com/2017
## day 18

from collections import deque
import re

RUNNING = 1
WAITING = 2
FINISHED = 3
PART_ONE = False
set_direct_re = re.compile("set (\w) (-?\d+)")
set_indirect_re = re.compile("set (\w) (\w)")


class Pipe:
    def __init__(self, id):
        self.id = id
        self.send_count = 0
        self.pipe = deque()

    def send(self, value):
        self.send_count += 1
        self.pipe.append(value)

    def receive(self):
        result = self.pipe.popleft()
        return result

    def is_empty(self):
        return len(self.pipe) == 0


class Puzzle:
    def __init__(self, id, lines, send_pipe, receive_pipe):
        self.id = id
        self.compile(lines)
        self.send_pipe = None
        self.receive_pipe = None
        self.reset()
        self.waiting = False
        self.send_pipe = send_pipe
        self.receive_pipe = receive_pipe
        self.state = RUNNING

    def reset(self):
        self.frequency = 0
        self.recovered_frequency = 0
        self.register_values = {}

        self.ip = 0
        for reg in self.register_names:
            self.register_values[reg] = 0

        self.register_values["p"] = self.id

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

    def mul(self, param):
        target, value = self.crack_two_params(param)
        self.register_values[target] *= value
        self.ip += 1

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

    def print_instruction(self, instruction):
        cmd = instruction[0]
        print(self.id, " --- ", self.ip, ": ", cmd, end=" ")
        for param in instruction[2]:
            print(param, end=" ")
        print()

    def execute(self):

        if self.state == FINISHED:
            return

        while 0 <= self.ip < len(self.instructions):
            self.state = RUNNING
            instruction = self.instructions[self.ip]
            instruction[1](instruction[2])
            if self.waiting:
                self.state = WAITING
                break

        if (self.ip < 0) or (self.ip >= len(self.instructions)):
            self.state = FINISHED
        return

    def can_proceed(self):
        if self.state == FINISHED:
            return False

        if self.waiting:
            if self.receive_pipe.is_empty():
                return False
        return True


def parse_input(lines):
    return lines


def part1(data):
    if not PART_ONE:
        return 0
    loopback = Pipe("loopback")
    puzzle = Puzzle(0, data, loopback, loopback)
    puzzle.execute()
    return puzzle.recovered_frequency


def part2(data):

    pipe01 = Pipe("0_send")
    pipe10 = Pipe("1_send")
    puzzle0 = Puzzle(0, data, pipe01, pipe10)
    puzzle1 = Puzzle(1, data, pipe10, pipe01)

    while puzzle0.can_proceed() or puzzle1.can_proceed():

        puzzle1.execute()
        puzzle0.execute()

    return pipe10.send_count
