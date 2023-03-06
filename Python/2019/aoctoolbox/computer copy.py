class Instruction:
    def __init__(self, name, func, params):
        self.name = name
        self.func = func
        self.params = params

class Computer:
    def __init__(self):
        self.reset()
        pass

    def reset(self):
        self.registers = {}
        self.ip = 0

    def compile(self, program, presplit = True):
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
    def print_instruction(self, ip):
        instruction = self.instructions[ip]
        print(ip, ":", instruction.name, end="")
        for param in instruction.params:
            print(" ", param, end="")
        print()
    def pre_instruction(self):
        pass
    def post_instruction(self):
        pass
    def run(self, verbose=False):
        while 0 <= self.ip < len(self.instructions):
            if(self.pre_instruction()):
                break
            if (verbose):                
                self.print_instruction(self.ip)                
            inst = self.instructions[self.ip]
            inst.func(*inst.params)
            self.post_instruction()

class BunnyComputer(Computer):
    def add(self, x, y):        
        adder = self.get_value(y)
        self.set_register(x,  self.get_register(x) + adder)
        self.ip += 1
    def sub(self, x, y):        
        adder = self.get_value(y)
        self.set_register(x,  self.get_register(x) - adder)
        self.ip += 1
    def mul(self, x,y):
        self.set_register(x, self.get_register(x) * self.get_value(y))
        self.ip += 1
    def div(self, x,y):
        self.set_register(x, self.get_register(x) // self.get_value(y))
        self.ip += 1
    def mod(self, x,y):
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
        if not(x_val == 0):
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
        
class IntcodeComputer():
    def __init__(self):
        self.original_program = []
        self.reset()
        
        self.instruction_set = {}

    def reset(self):
        self.program = self.original_program.copy()
        self.ip = 0

    def set_instruction_set(self, instruction_set):
        self.instruction_set = instruction_set

    def load(self, program):        
        self.original_program = program
        self.reset()

    def print_instruction(self, ip, instruction):        
        print(ip, ":", instruction.name, end="")
        for param in instruction.params:
            print(" ", param, end="")
        print()

    def __getitem__(self, k):
        return self.program[k]

    def __setitem__(self, k, value):  
        self.program[k] = value

    def decode_instruction(self, ip):
        instruction = self.program[ip]
        func, param_count = self.instruction_set[instruction]
        return Instruction(instruction, func, self.program[ip+1:ip+1+param_count])        
    
    def pre_instruction(self):
        pass

    def post_instruction(self):
        pass

    def run(self, verbose=False):
        while 0 <= self.ip < len(self.program):
            if(self.pre_instruction()):
                break
            instruction = self.decode_instruction(self.ip)
            if (verbose):                
                self.print_instruction(self.ip, instruction)                    
            instruction.func(*instruction.params)
            self.post_instruction()
        

def run():
    print("computer loaded successfully")