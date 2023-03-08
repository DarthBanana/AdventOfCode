from computer import *
from collections import deque


class IntCodeParameter(Parameter):
    
    def __new__(self, mode, raw_value, address, value, destination=False):
        self.mode = mode
        return Parameter.__new__(self, raw_value, address, value, destination)
    
    def __init__(self, mode, raw_value, address, value, destination=False):
        self.mode = mode
        
        return Parameter.__init__(self, raw_value, address, value, destination)

    def __str__(self):
        if self.mode == 0:
            return "I{0}({1})".format(self.raw, int(self))
        elif self.mode == 1:
            return "D{0}".format(self.raw)
        elif self.mode == 2:
            return "R{0}({1})".format(self.raw, int(self))
    
    def interpret(self):  
        #print("INTERPRET", self.mode, self.raw, self.address, int(self), self.destination)      
        if self.mode == 0:
            return "M{0}".format(self.raw)
        elif self.mode == 1:
            if self.destination:
                return "M{0}".format(self.raw)
            return str(int(self))
        elif self.mode == 2:
            if self.destination:
                return "M(base + {0})".format(self.raw)
            return "(base + {0})".format(self.raw)

class IntcodeInstructionDescriptor(InstructionDescriptor):
    def __init__(self, name, func, param_count, output_param_number, format_string):
        self.param_count = param_count
        self.output_param_number = output_param_number
        
        return InstructionDescriptor.__init__(self, name, func, format_string)
    

    
class Mailbox:
    def __init__(self, verbose=False):
        self.mailbox = deque()
        self.verbose = verbose
        self.chained_output = None        
    def send(self, value: int):
        value = int(value)
        if self.verbose:
            print("SEND",value)
        if self.chained_output is not None:
            self.chained_output.send(value)
        else:
            self.mailbox.append(value)
    def chain_output(self, mailbox):
        self.chained_output = mailbox
    def receive(self):
        if len(self.mailbox) == 0:
            return None
        result = self.mailbox.popleft()
        if self.verbose:
            print("RECV",result)
        return result
    def __len__(self):
        return len(self.mailbox)
    def __str__(self):
        return str(list(self.mailbox))
    def reset(self):
        self.mailbox = deque()
    
class IntcodeComputer(ComputerRoot):
    def __init__(self):
        super().__init__()                
        self.instruction_set = {}
        

    def reset(self):        
        super().reset()    
        self.relative_base = 0            
        self.program = self.original_program.copy()
        self.memory = {}
        for i in range(len(self.original_program)):
            self.memory[i] = self.original_program[i]
            
        
        

    def set_instruction_set(self, instruction_set):
        self.instruction_set = instruction_set

    def __getitem__(self, k): 
        if isinstance(k, Parameter):
            #print("GET", k.raw, self.memory.get(k.raw, 0))
            return self.memory.get(k.address, 0)
        else:
            value = self.memory.get(k, 0)
            #print("GET", k, value)
        return self.memory.get(k, 1)

    def __setitem__(self, k, value):                  
        if isinstance(k, Parameter):
            #print("SET", k.raw, value)
            self.memory[k.address] = value
        else:
            #print("SET", k, value)
            self.memory[k] = value

    def is_ip_valid(self, ip):
        if ip < 0:
            return False
        if ip not in self.memory:
            return False
        return True
    
    def get_parameter(self, ip, offset, mode, destination=False):
        raw_value = self[ip + offset]        
        if mode == 0:
            address = raw_value
            value = self[address]            
        elif mode == 1:
            address = -1
            value = raw_value            
        elif mode == 2:
            address = raw_value + self.relative_base
            value = self[address]            
        else:
            raise Exception("Invalid mode {0}".format(mode))
        return IntCodeParameter(mode, raw_value, address, value, destination)

    def interpret_instruction(self, instruction):        
        inst_descriptor = self.instruction_set[instruction.opcode]
        format_string = inst_descriptor.format_string
        params = instruction.params                
        param_values = [p.interpret() for p in params]        
        return format_string.format(*param_values)

    def get_instruction(self, ip):   
         
        instruction = self.memory[ip]
        opcode = instruction % 100
        if opcode not in self.instruction_set:
            return None
        inst_descriptor = self.instruction_set[opcode]
        func = inst_descriptor.func
        param_count = inst_descriptor.param_count
        output_param_index = inst_descriptor.output_param_number - 1
                
        params = []
        for i in range(param_count):
            mode = instruction % 10**(i+3) // 10**(i+2)            
            param = self.get_parameter(ip, i+1, mode, output_param_index == i)
            params.append(param)
            param = 0                    

        return Instruction(instruction, func, params, opcode)
    
    def advance_to_next_instruction(self, ip, instruction):
        return ip + len(instruction.params) + 1
    
    
    
class MyIntcodeComputer(IntcodeComputer):
    def __init__(self, rx_mailbox, tx_mailbox):
        self.tx_mailbox = tx_mailbox
        self.rx_mailbox = rx_mailbox
        IntcodeComputer.__init__(self)
        self.instmap = {
            1:IntcodeInstructionDescriptor("add", self.add, 3, 3, "{2} = {0} + {1}"), 
            2:IntcodeInstructionDescriptor("mul", self.mul, 3, 3, "{2} = {0} * {1}"), 
            3:IntcodeInstructionDescriptor("rcv", self.rcv, 1, 1, "{0} = rx"),
            4:IntcodeInstructionDescriptor("tx", self.tx, 1, 0, "tx({0})"), 
            5:IntcodeInstructionDescriptor("jit", self.jit, 2, 0, "if {0} != 0: GOTO {1}"),
            6:IntcodeInstructionDescriptor("jif", self.jif, 2, 0, "if {0} == 0: GOTO {1}"),
            7:IntcodeInstructionDescriptor("lt", self.lt, 3, 3, "{2} = 1 if {0} < {1} else 0"),
            8:IntcodeInstructionDescriptor("eq", self.eq, 3, 3, "{2} = 1 if {0} == {1} else 0"),
            9:IntcodeInstructionDescriptor("srb", self.srb, 1, 0, "base += {0}"),
            99:IntcodeInstructionDescriptor("halt", self.halt, 0, 0, "halt")}
        self.set_instruction_set(self.instmap)


    def reset(self):
        IntcodeComputer.reset(self)
        self.rx_mailbox.reset()
        self.tx_mailbox.reset()

    def add(self, x, y, z):
        self[z] = x + y
        self.ip += 4

    def mul(self, x, y, z):
        self[z] = x * y
        self.ip += 4

    def jit(self, x, y):
        if x != 0:
            self.ip = y
        else:
            self.ip += 3
    
    def jif(self, x, y):
        if x == 0:
            self.ip = y
        else:
            self.ip += 3
    
    def lt(self, x, y, z):
        if x < y:
            self[z] = 1
        else:
            self[z] = 0
        self.ip += 4
    
    def eq(self, x, y, z):
        if x == y:
            self[z] = 1
        else:
            self[z] = 0
        self.ip += 4
    def srb(self, x):        
        self.relative_base += x
        if self.verbose:
            print("relative base", self.relative_base)
        self.ip += 2

    def halt(self):
        self.ip = -1

    def rcv(self, x):

        if len(self.rx_mailbox) == 0:
            self.enter_wait_state()
            if self.verbose:
                print("waiting for input")
            return
        self[x] = self.rx_mailbox.receive()        
        self.ip += 2

    def tx(self, x):        
        self.tx_mailbox.send(x)
        self.ip += 2