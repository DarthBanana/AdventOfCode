from computer import *
from collections import deque
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
            return self.memory.get(k.raw, 0)
        else:
            value = self.memory.get(k, 0)
            #print("GET", k, value)
        return self.memory.get(k, 1)

    def __setitem__(self, k, value):                  
        if isinstance(k, Parameter):
            #print("SET", k.raw, value)
            self.memory[k.raw] = value
        else:
            #print("SET", k, value)
            self.memory[k] = value

    def is_ip_valid(self, ip):
        return 0 <= ip 

    def get_instruction(self, ip):        
        instruction = self.memory[ip]
        opcode = instruction % 100
        
        func, param_count = self.instruction_set[opcode]
        params = []
        for i in range(param_count):
            param = self.memory[ip + 1 + i]
            
            mode = instruction % 10**(i+3) // 10**(i+2)
            if mode == 0:
                params.append(Parameter(param, self[param]))
            elif mode == 1:
                params.append(Parameter(param, param))
            elif mode == 2:
                address = param + self.relative_base
                #print("REL", param, self.relative_base, address, self[address])
                params.append(Parameter(address, self[address]))
        return Instruction(instruction, func, params)
    
    
class MyIntcodeComputer(IntcodeComputer):
    def __init__(self, rx_mailbox, tx_mailbox):
        self.tx_mailbox = tx_mailbox
        self.rx_mailbox = rx_mailbox
        IntcodeComputer.__init__(self)
        self.instmap = {
            1:(self.add, 3), 
            2:(self.mul, 3), 
            3:(self.rcv, 1),
            4:(self.tx, 1), 
            5:(self.jit, 2),
            6:(self.jif, 2),
            7:(self.lt, 3),
            8:(self.eq, 3),
            9:(self.srb, 1),
            99:(self.halt, 0)}
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