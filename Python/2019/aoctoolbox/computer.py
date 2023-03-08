#
# TODOs: Add debugging support
#       Add support for breakpoints
#       Add support for stepping
#       Add support for compiler optimization
#       Add support for waiting state (thread scheduling?)
#

import operator

class Instruction:
    def __init__(self, name, func, params, opcode=None):
        self.name = name
        self.func = func
        self.params = params
        self.opcode = opcode
    def __str__(self):
        output = str(self.name)        
        for param in self.params:            
            output += " " + str(param)        
        return output
        
    
    def execute(self):
        self.func(*self.params)
    

class ComputerRoot:
    def __init__(self):
        
        self.breakpoints = set()
        self.original_program = []
        self.reset()

    def reset(self):      
        self.verbose = False
        self.running = False        
        self.ip: int = 0    
    
    def load_program(self, program, reset=True):
        self.original_program = program       
        if reset:
            self.reset() 
    
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
    
    def get_instruction(self, ip):
        return None
    
    def run_instruction(self, instruction):
        pass

    def print_instruction(self, instruction, ip):        
        
        print(int(ip), ":", instruction)        

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
                #print("Invalid IP:", self.ip)
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

            instruction.execute()

            if self.post_instruction(instruction):
                self.running = False
                break
            


    

    
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




        

def run():
    print("computer loaded successfully")