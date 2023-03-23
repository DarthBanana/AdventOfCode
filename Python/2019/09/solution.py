## advent of code 2019
## https://adventofcode.com/2019
## day 09

from aocpuzzle import *
from intcode import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)        
        self.computer = MyIntcodeComputer()
        self.computer.load_program_from_input(lines)
        
        
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
        if (self.is_test):
            return str(self.computer.tx_mailbox)
        print(self.computer.tx_mailbox)
        return self.check_diagnostic_output(self.computer.tx_mailbox)


    def part2(self):
        self.computer.reset()
        self.computer.rx_mailbox.send(2)

        self.computer.run(False)

        print(self.computer.tx_mailbox)
        return self.check_diagnostic_output(self.computer.tx_mailbox)