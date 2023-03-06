## advent of code 2019
## https://adventofcode.com/2019
## day 05

from collections import deque
from aocpuzzle import *
from computer import *
from parsehelp import *
class Mailbox:
    def __init__(self):
        self.mailbox = deque()
    def send(self, value: int):
        value = int(value)
        print("SEND",value)
        self.mailbox.append(value)
    def receive(self):
        if len(self.mailbox) == 0:
            return None
        return self.mailbox.popleft()
    def __len__(self):
        return len(self.mailbox)
    def __str__(self):
        return str(self.mailbox)
    
class MyIntcodeComputer(IntcodeComputer):
    def __init__(self):
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
            99:(self.halt, 0)}
        self.set_instruction_set(self.instmap)
        self.tx_mailbox = None
        self.rx_mailbox = None

    def set_tx_mailbox(self, mailbox):
        self.tx_mailbox = mailbox
    def set_rx_mailbox(self, mailbox):
        self.rx_mailbox = mailbox

    def reset(self):
        IntcodeComputer.reset(self)
        self.incoming_mailbox = deque()

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

    def halt(self):
        self.ip = -1

    def rcv(self, x):

        if len(self.rx_mailbox) == 0:
            self.enter_wait_state()
            print("waiting for input")
            return
        self[x] = self.rx_mailbox.receive()
        print("received", self[x])
        self.ip += 2

    def tx(self, x):
        print("sending", x)
        self.tx_mailbox.send(x)
        self.ip += 2


class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test = False):
        AoCPuzzle.__init__(self, lines, is_test)        
        if self.is_test:
            print("test")
            inputline = lines.pop(0)
            self.input_value = int(inputline)
        else:
            self.input_value = 5
        self.code = get_all_ints(lines[0])
        
    def check_diagnostic_output(self, output_mailbox):
        while len(output_mailbox):
            val = output_mailbox.receive()
            if len(output_mailbox) == 0:
                break
            if not val == 0:
                print("ERROR")
                return False
        return val

    def part1(self):
        tx_mailbox = Mailbox()
        rx_mailbox = Mailbox()
        computer = MyIntcodeComputer()
        computer.set_tx_mailbox(rx_mailbox)
        computer.set_rx_mailbox(tx_mailbox)        
        code = self.code.copy()        
        computer.load_program(code)
        computer.reset()
        tx_mailbox.send(1)
        
        computer.run(True)
        
        return self.check_diagnostic_output(rx_mailbox)

    def part2(self):
        tx_mailbox = Mailbox()  
        rx_mailbox = Mailbox()
        computer = MyIntcodeComputer()
        computer.set_tx_mailbox(rx_mailbox)
        computer.set_rx_mailbox(tx_mailbox)
        code = self.code.copy()
        computer.load_program(code)
        computer.reset()
        tx_mailbox.send(self.input_value)

        computer.run(True)
        return self.check_diagnostic_output(rx_mailbox)
    