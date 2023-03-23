## advent of code 2019
## https://adventofcode.com/2019
## day 05


from aocpuzzle import *
from parsehelp import *
from intcode import *

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
        self.computer = MyIntcodeComputer()
        self.computer.load_program(self.code)

        
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

        self.computer.reset()
        self.computer.rx_mailbox.send(1)
        
        self.computer.run(True)
        
        return self.check_diagnostic_output(self.computer.tx_mailbox)

    def part2(self):        
        self.computer.reset()
        self.computer.rx_mailbox.send(self.input_value)

        self.computer.run(True)
        return self.check_diagnostic_output(self.computer.tx_mailbox)
    