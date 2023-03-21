#
# TODOs: Add debugging support
#       Add support for breakpoints
#       Add support for stepping
#       Add support for compiler optimization
#       Add support for waiting state (thread scheduling?)
#

import operator


class Parameter(int):

    def __new__(self, raw_value, address, value, destination=False):
        self.raw = raw_value
        self.address = address
        self.destination = destination
        self.my_value = value
        if destination:
            self.my_value = address
        return int.__new__(self, self.my_value)

    def __init__(self, raw_value, address, value, destination=False):
        self.raw = raw_value
        self.address = address
        self.destination = destination
        self.my_value = value
        if destination:
            self.my_value = address
        int.__init__(self)

    def __str__(self):
        return "{0}({1})".format(self.raw, int(self))

    def __repr__(self):
        return str(self)

    def interpret(self):
        return str(self)


class InstructionDescriptor:
    def __init__(self, name, func, format_string):
        self.name = name
        self.func = func
        self.format_string = format_string


class Instruction:
    def __init__(self, name, func, params, opcode=None, ip=0):
        self.ip = ip
        self.name = name
        self.func = func
        self.params = params
        self.opcode = opcode

    def __str__(self):
        output = "{}".format(self.name)
        for param in self.params:
            output += " " + str(param)
        return output

    def execute(self):
        self.func(*self.params)


class ComputerRoot:
    def __init__(self):

        self.breakpoints = set()
        self.original_program = []
        self.instruction_descriptors = {}
        self.trace_enabled = False
        self.trace_file = None
        self.trace_ip_only = False
        self.reset()

    def reset(self):
        self.verbose = False
        self.running = False
        self.ip: int = 0

    def load_program(self, program, reset=True):
        self.original_program = program
        if reset:
            self.reset()

    def enable_execution_trace(self, filename="trace.txt", ip_only=False):
        self.trace_enabled = True
        self.trace_file = open(filename, "w")
        self.trace_ip_only = ip_only

    def disable_execution_trace(self):
        self.trace_enabled = False
        if self.trace_file:
            self.trace_file.close()
            self.trace_file = None

    def set_breakpoint(self, breakpoint):
        self.breakpoints.add(breakpoint)

    def clear_breakpoint(self, breakpoint):
        self.breakpoints.remove(breakpoint)

    def clear_all_breakpoints(self):
        self.breakpoints.clear()

    def go(self):
        self.running = True

    def stop(self):
        self.running = False

    def step(self):
        self.running = False
        self.run()

    def is_ip_valid(self, ip):

        return True

    def pre_instruction(self, instruction):
        return False

    def post_instruction(self, instruction):
        return False

    def get_instruction(self, ip, for_interpretation=False):
        return None

    def run_instruction(self, instruction):
        pass

    def get_instruction_string(self, instruction, ip):
        return "{0}:{1}".format(ip, instruction)

    def print_instruction(self, instruction, ip):
        print(self.get_instruction_string(instruction, ip))

    def enter_wait_state(self):
        self.running = False

    def can_continue(self):
        if self.is_ip_valid(self.ip) == False:
            return False
        return True

    def run(self, verbose=False):
        self.running = True
        self.verbose = verbose
        while self.running:

            if self.is_ip_valid(self.ip) == False:
                # print("Invalid IP:", self.ip)
                self.running = False
                break

            if self.ip in self.breakpoints:
                self.running = False
                print("Breakpoint hit at", self.ip, "")

            instruction = self.get_instruction(self.ip)
            if instruction is None:
                print("Invalid instruction at", self.ip)
                self.running = False
                break

            if self.pre_instruction(instruction):
                self.running = False
                break

            if verbose:
                self.print_instruction(instruction, self.ip)

            if self.trace_enabled:
                if self.trace_ip_only:
                    self.trace_file.write(str(self.ip))
                else:
                    trace_string = "{0: <30}{1:<30}\n".format(self.get_instruction_string(
                        instruction, self.ip), self.interpret_instruction(instruction))
                    self.trace_file.write(trace_string)

            instruction.execute()

            if self.post_instruction(instruction):
                self.running = False
                break

    def advance_to_next_instruction(self, ip, instruction):
        return ip + 1

    def interpret_instruction(self, instruction):
        inst_descriptor = self.instruction_set[instruction.opcode]
        format_string = inst_descriptor.format_string
        params = instruction.params
        param_values = [p.interpret() for p in params]
        return format_string.format(*param_values)

    def interpret_program(self):
        ip = 0
        while self.is_ip_valid(ip):

            instruction = self.get_instruction(ip, True)
            if instruction is None:
                print(ip, ":\t !!!!! Invalid opcode {0} !!!!!".format(
                    self.memory[ip]))
                ip += 1
                continue

            # print(ip, instruction)
            print(ip, ":\t", self.interpret_instruction(instruction))

            ip = self.advance_to_next_instruction(ip, instruction)


class Computer(ComputerRoot):
    def __init__(self):
        super().__init__()
        

    def reset(self):
        super().reset()
        self.registers = {}
        self.ip = 0

    def compile(self, program, presplit=True):
        if presplit:
            lines = program
        else:
            lines = program.splitlines()
        self.instructions = []

        for line in lines:
            trimmed = line.strip()
            if len(trimmed) == 0:
                continue
            inst = self.crack_instruction(trimmed)
            self.instructions.append(inst)

    def func_name_conversion(self, command):
        return command

    def command_conversion(self, items):
        return items

    def crack_instruction(self, line):
        split = line.split()
        split = self.command_conversion(split)
        command = self.func_name_conversion(split.pop(0))
        func = getattr(self, command)
        inst = Instruction(command, func, split)
        return inst

    def set_register(self, name, value):
        self.registers[name] = value

    def __getitem__(self, k):
        return self.registers.get(k, 0)

    def __setitem__(self, k, value):
        self.set_register(k, value)

    def get_register(self, name):
        if name in self.registers.keys():
            return self.registers[name]
        else:
            return 0

    def get_value(self, param):
        if param.isalpha():
            return self.get_register(param)
        else:
            return int(param)
    
    def is_ip_valid(self, ip):
        if 0 <= ip < len(self.instructions):            
            return True
        return False

    def get_instruction(self, ip):
        return self.instructions[ip]

    

class BunnyComputer(Computer):
    def add(self, x, y):
        adder = self.get_value(y)
        self.set_register(x,  self.get_register(x) + adder)
        self.ip += 1

    def sub(self, x, y):
        adder = self.get_value(y)
        self.set_register(x,  self.get_register(x) - adder)
        self.ip += 1

    def mul(self, x, y):
        self.set_register(x, self.get_register(x) * self.get_value(y))
        self.ip += 1

    def div(self, x, y):
        self.set_register(x, self.get_register(x) // self.get_value(y))
        self.ip += 1

    def mod(self, x, y):
        self.set_register(x, self.get_register(x) % self.get_value(y))
        self.ip += 1

    def set(self, x, y):
        self.set_register(x, self.get_value(y))
        self.ip += 1

    def cpy(self, x, y):
        self.set_register(x, self.get_value(y))
        self.ip += 1

    def jgz(self, x, y):
        x_val = self.get_value(x)
        y_val = self.get_value(y)
        if x_val > 0:
            self.ip += y_val
        else:
            self.ip += 1

    def jnz(self, x, y):
        x_val = self.get_value(x)
        y_val = self.get_value(y)
        if not (x_val == 0):
            self.ip += y_val
        else:
            self.ip += 1

    def jz(self, x, y):
        x_val = self.get_value(x)
        y_val = self.get_value(y)
        if (x_val == 0):
            self.ip += y_val
        else:
            self.ip += 1

    def jmp(self, y):
        y_val = self.get_value(y)
        self.ip += y_val


def run():
    print("computer loaded successfully")
