## advent of code 2019
## https://adventofcode.com/2019
## day 09

from aocpuzzle import *
from intcode import *
from parsehelp import *

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)        
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
        computer = MyIntcodeComputer(tx_mailbox, rx_mailbox)
        
        code = self.code.copy()        
        computer.load_program(code)
        computer.reset()
        tx_mailbox.send(1)
        
        computer.run(True)
        
        return self.check_diagnostic_output(rx_mailbox)


    def part2(self):
        pass